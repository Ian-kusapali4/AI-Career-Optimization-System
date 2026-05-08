from unittest import result

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from Job_match.agents.json_schema.Career_architect_schema import CareerPath
from services.parser.yaml_parser import yaml_extraction
from Core.Unifiedstate import IndigoMasterState 
from Core.model_factory import get_model



#agent set to generating career path suggestions 

my_model = get_model()

def generate_career_suggestions(profile_data: dict):

    """
    Takes CandidateProfile object and YAML config dictionary.
    Returns a CareerPath object with titles and reasons.
    """
    if not profile_data:
        raise ValueError("No profile data provided to generate suggestions")

    config_data = yaml_extraction('Jobalocation.yaml')
    template_str = config_data['prompt_configuration']['template']
    prompt_template = ChatPromptTemplate.from_template(template_str)

    structured_llm = my_model.with_structured_output(CareerPath, method="json_mode")
    chain = prompt_template | structured_llm
    
    return chain.invoke(profile_data)

def suggested_Job_formating(state: IndigoMasterState):

    profile_to_process = state.Profile 
    result = generate_career_suggestions(profile_to_process)
    return {"search_queries": result.model_dump()}