from unittest import result

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from agents.json_schema.Career_architect_schema import CareerPath
from services.parser.yaml_parser import yaml_extraction
from core.Nodes.GraphState import GraphState
from core.model_factory import get_model



#agent set to generating career path suggestions 

# Set up the model
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

    # Invoke with the clean dictionary
    return chain.invoke(profile_data)

def suggested_Job_formating(state: GraphState):

    profile_to_process = state.Profile 
    result = generate_career_suggestions(profile_to_process)
    return {"search_queries": result.model_dump()}