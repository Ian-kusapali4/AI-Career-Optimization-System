from Core.model_factory import get_model
from langchain_core.prompts import ChatPromptTemplate

from Core.Unifiedstate import CandidateProfile
from langchain_core.output_parsers import PydanticOutputParser
from services.parser.yaml_parser import yaml_extraction
from Core.Unifiedstate import IndigoMasterState

#Resume extraction agent, takes resume data and extracts the relevant fields
my_model = get_model()
print("--- Loading Resume_extraction_agent.py ---")
config_data = yaml_extraction('auditor.yaml')

def Resume_extaction(state: IndigoMasterState = None):
    """Extracted relevant information from the candidate's resume."""
    if state is None or not state.get("raw_resume"):
        print("❌ ERROR: No resume text found in state!")
        return {}

    # 1. Load the templates
    # Ensure {format_instructions} is removed from these strings in your YAML
    full_template = f"{config_data['system_message']}\n\n{config_data['user_template']}"
    prompt_template = ChatPromptTemplate.from_template(full_template)
    
    # 2. Bind the structured output
    structured_llm = my_model.with_structured_output(CandidateProfile)
    
    chain = prompt_template | structured_llm
    
    # 3. Invoke with ONLY the remaining variable
    try:
        response = chain.invoke({
            "resume_text": state.get("raw_resume")
        })
        
        # 4. Convert to dict for the State
        if hasattr(response, 'model_dump'):
            profile_dict = response.model_dump()
        elif isinstance(response, dict):
            profile_dict = response
        else:
            # Fallback for unexpected formats
            profile_dict = dict(response)

        print(f"🔍 DEBUG: CandidateProfile extracted successfully!")
        return {"CandidateProfile": profile_dict}

    except Exception as e:
        print(f"❌ Extraction Node Failed: {e}")
        return {}