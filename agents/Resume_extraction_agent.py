import json
import re
import unicodedata
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

    system_msg = config_data['system_message'] + "\nSTRICT: Return ONLY raw JSON. No markdown."
    full_template = f"{system_msg}\n\n{config_data['user_template']}"
    prompt_template = ChatPromptTemplate.from_template(full_template)
    
    structured_llm = my_model.with_structured_output(CandidateProfile)
    chain = prompt_template | structured_llm
    
    try:
        response = chain.invoke({"resume_text": state.get("raw_resume")})
        profile_dict = response.model_dump() if hasattr(response, 'model_dump') else dict(response)
        print(f"🔍 DEBUG: CandidateProfile extracted successfully!")
        return {"CandidateProfile": profile_dict}

    except Exception as e:
        print(f"⚠️ EXTRACTION NODE: Standard parsing failed, attempting greedy recovery...")
        error_str = str(e)
        
        try:
            # 1. Clean the string of bad unicode/non-breaking spaces first
            cleaned_err = unicodedata.normalize("NFKC", error_str)
            
            # 2. GREEDY REGEX: Find the FIRST '{' and the LAST '}'
            # This ignores everything outside the main JSON block, 
            # effectively deleting the 'Extra data' (like those trailing }})
            json_match = re.search(r'(\{.*\})', cleaned_err, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1).strip()
                
                # 3. Clean up internal escape characters that often break LLM tool calls
                json_str = json_str.replace("\\n", " ").replace('\\"', '"')
                
                # 4. Parse the isolated JSON block
                data = json.loads(json_str)
                
                # Handle cases where it's wrapped in 'arguments' or 'properties'
                if isinstance(data, dict):
                    if "arguments" in data:
                        recovered_profile = data["arguments"]
                    elif "properties" in data:
                        recovered_profile = data["properties"]
                    else:
                        recovered_profile = data
                else:
                    raise ValueError("Extracted JSON is not a dictionary")

                print("♻️ RECOVERY SUCCESS: CandidateProfile isolated and parsed.")
                return {"CandidateProfile": recovered_profile}
                
        except Exception as recovery_err:
            print(f"🚫 RECOVERY FAILED: {recovery_err}")

        print(f"❌ Extraction Node Permanently Failed: {e}")
        return {"CandidateProfile": {}, "error_message": str(e)}