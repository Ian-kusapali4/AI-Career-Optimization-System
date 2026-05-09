import json
from Core.model_factory import get_model
from langchain_core.prompts import ChatPromptTemplate
from Core.Unifiedstate import CandidateProfile, IndigoMasterState
from services.parser.yaml_parser import yaml_extraction

my_model = get_model()
config_data = yaml_extraction('auditor.yaml')

def Resume_extaction(state: IndigoMasterState = None):
    """Extracted relevant information from the candidate's resume."""
    if state is None or not state.get("raw_resume"):
        print("❌ ERROR: No resume text found in state!")
        return {}

    full_template = f"{config_data['system_message']}\n\n{config_data['user_template']}"
    prompt_template = ChatPromptTemplate.from_template(full_template)
    
    # Keeping structured approach
    structured_llm = my_model.with_structured_output(CandidateProfile)
    chain = prompt_template | structured_llm
    
    try:
        response = chain.invoke({"resume_text": state.get("raw_resume")})
        profile_dict = response.model_dump() if hasattr(response, 'model_dump') else dict(response)
        print(f"🔍 DEBUG: CandidateProfile extracted successfully!")
        return {"CandidateProfile": profile_dict}

    except Exception as e:
        print(f"⚠️ EXTRACTION NODE: Standard parsing failed, attempting recovery...")
        error_str = str(e)
        
        if "failed_generation" in error_str:
            try:
                # 1. Isolate the JSON string from the error body
                start_marker = "'failed_generation': '"
                # Find the end of the string, avoiding trailing markers
                raw_json = error_str.split(start_marker)[1].split("'}}")[0]
                
                # 2. Clean up escape characters
                clean_json = raw_json.replace("\\n", "").replace("\\", "")
                data = json.loads(clean_json)
                
                # 3. Handle Tool Call structure (as seen in your logs)
                # Your logs show: {"name": "CandidateProfile", "arguments": {...}}
                if isinstance(data, dict) and "arguments" in data:
                    recovered_profile = data["arguments"]
                else:
                    recovered_profile = data
                
                print("♻️ RECOVERY SUCCESS: Extracted data from Tool Call error body.")
                return {"CandidateProfile": recovered_profile}
                
            except Exception as recovery_err:
                print(f"🚫 RECOVERY FAILED: {recovery_err}")

        print(f"❌ Extraction Node Permanently Failed: {e}")
        return {"error_message": str(e)}