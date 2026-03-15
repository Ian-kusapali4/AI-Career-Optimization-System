from core.model_factory import get_model
from langchain_core.prompts import ChatPromptTemplate

from agents.json_schema.resume_extraction_schema import CandidateProfile
from langchain_core.output_parsers import PydanticOutputParser
from services.parser.yaml_parser import yaml_extraction
from core.Nodes.GraphState import GraphState

#Resume extraction agent, takes resume data and extracts the relevant fields
my_model = get_model()
print("--- Loading Resume_extraction_agent.py ---")
config_data = yaml_extraction('auditor.yaml')

def Resume_extaction(state:GraphState=None):
    """This agent is responsible for extracting relevant information from the candidate's resume. It takes the raw resume text as input and produces a structured CandidateProfile object that includes key details such as skills, experience, and education."""

    if state is None:
        print("❌ ERROR: State reached the node as None!")
        return {}

    parser = PydanticOutputParser(pydantic_object=CandidateProfile)
    format_instructions = parser.get_format_instructions()
    full_template = f"{config_data['system_message']}\n\n{config_data['user_template']}"
    prompt_template = ChatPromptTemplate.from_template(full_template)
    structured_llm = my_model.with_structured_output(CandidateProfile)
    
    chain = prompt_template | structured_llm
    response = chain.invoke({
        "resume_text": state.raw_resume,
        "format_instructions": format_instructions
    })
    profile_dict = response.model_dump() 

    print(f"🔍 DEBUG: CandidateProfile extracted successfully: {profile_dict} ❌ CandidateProfile 1")

    return {"CandidateProfile": profile_dict}
