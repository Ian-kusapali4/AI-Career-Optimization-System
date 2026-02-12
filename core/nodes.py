from agents.auditor_logic import run_auditor_llm,yaml_extraction
from langchain_core.prompts import ChatPromptTemplate
from agents.json_schema.json_schema import CandidateProfile
from langchain_ollama import ChatOllama
from schema import GraphState



#compliation of all the nodes in the system 
config_data = yaml_extraction()
my_model = ChatOllama(model="llama3.1:8b", temperature=0, format='json')



def auditor_node(state: GraphState):
    # 1. Get data from State
    text = state["raw_resume_text"]
    notes = state.get("user_context_notes", "")
    
    
    structured_llm = my_model.with_structured_output(CandidateProfile)
    full_template = f"{config_data['system_message']}\n\n{config_data['user_template']}"
    prompt_template = ChatPromptTemplate.from_template(full_template)
        
    
    # 3. Call the Agent Logic
    result = run_auditor_llm(structured_llm, prompt_template, text, notes)
    
    # 4. Update the State
    return {"master_profile": result}