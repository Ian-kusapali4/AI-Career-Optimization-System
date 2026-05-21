import json
import re
import sys
import time  # Added for network pacing
from langchain_core.prompts import ChatPromptTemplate
from Core.model_factory import get_model
from Core.Unifiedstate import CandidateProfile, ElevateMasterState
from services.parser.yaml_parser import yaml_extraction
from services.rag.ingestion import ingest_resume_to_chroma
from services.rag.retrieval import retrieve_focused_context

config_data = yaml_extraction('auditor.yaml')

def clean_llm_json(s):
    match = re.search(r'\{.*\}', s, re.DOTALL)
    return match.group(0) if match else s

def Resume_extaction(state: ElevateMasterState = None):
    print("\n=== DEBUGGING NODE STATE & PAYLOADS ===")
    if state is None or not state.get("raw_resume"):
        print("❌ ERROR: No raw_resume text found in state!")
        return {"CandidateProfile": {"skills": [], "jobTitle": "Unknown"}}

    resume_size = len(state.get("raw_resume", ""))
    print(f"📥 INCOMING STATE: raw_resume is {resume_size} characters.")

    vector_db = None 
    try:
        # --- PHASE 1 & 2: RAG PIPELINE ---
        print("📦 RAG: Initializing ChromaDB vector store injection...")
        vector_db = ingest_resume_to_chroma(state["raw_resume"])
        
        print("🔍 RAG: Executing schema-driven vector queries...")
        focused_context = retrieve_focused_context(vector_db)
        
        context_size = len(focused_context) if focused_context else 0
        print(f"🗃️ RETRIEVED CONTEXT: {context_size} characters prepared.")
        
        if not focused_context or not focused_context.strip():
            raise ValueError("RAG pipeline returned empty context.")

        # --- FIX 1: THE OLLAMA BREATHER ---
        # Give the local Ollama service 2 seconds to clear its queue and 
        # shut down the embedding connections before we open the LLM connection.
        print("⏳ Pacing: Giving Ollama 2 seconds to flush embedding sockets...")
        time.sleep(2)

        # --- PHASE 3: STATE PARSING ---
        print("🤖 RAG: Passing sanitized context chunks to LLM...")
        system_msg = (
            config_data['system_message'] + 
            "\nSTRICT: Respond ONLY with a valid JSON object. "
            "No markdown, no conversation."
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_msg),
            ("user", "Extract data variables strictly using this context block:\n\n{focused_context}")
        ])
        
        # --- FIX 2: FRESH PORT INSTANTIATION ---
        # Instantiating the model here ensures a brand new, isolated HTTP client 
        # is generated specifically for this call, preventing socket pollution.
        fresh_model = get_model()
        chain = prompt | fresh_model
        
        response = chain.invoke({"focused_context": focused_context})
        
        raw_output = response.content if hasattr(response, 'content') else str(response)
        print(f"📨 LLM RESPONSE: {len(raw_output)} characters received.")
        
        match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        if not match:
            raise ValueError("LLM response did not contain JSON.")
            
        cleaned_json = clean_llm_json(match.group(0))
        extracted_data = json.loads(cleaned_json)
        
        print("✅ RAG Extraction Pipeline Successful")
        return {"CandidateProfile": extracted_data}

    except Exception as e:
        print(f"⚠️ EXTRACTION NODE FAILURE: {e}")
        return {"CandidateProfile": {"skills": [], "jobTitle": "Unknown"}}

    finally:
        if vector_db is not None:
            try:
                vector_db.delete_collection()
                print("🧹 RAG: Vector database collection cleared.")
            except Exception as cleanup_err:
                print(f"⚠️ Cleanup warning: {cleanup_err}")