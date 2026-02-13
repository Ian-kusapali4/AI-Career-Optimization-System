from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from agents.json_schema.Career_architect_schema import CareerPath
from services.parser.yaml_parser import yaml_extraction

#agent set to generating career path suggestions 

# Set up the model
config = yaml_extraction('config.yaml')
if config is None:
    print("Critical Error: Configuration could not be loaded. Exiting.")
    exit(1) 
model_name = config['model_settings']['name']

my_model = ChatOllama(model=model_name)

def generate_career_suggestions(candidate_profile, config_data):
    """
    Takes CandidateProfile object and YAML config dictionary.
    Returns a CareerPath object with titles and reasons.
    """
    # Preparing the data Template
    template_str = config_data['prompt_configuration']['template']
    prompt_template = ChatPromptTemplate.from_template(template_str)
    

    structured_llm = my_model.with_structured_output(CareerPath, method="json_mode")
   
    chain = prompt_template | structured_llm
    
   
    result = chain.invoke(candidate_profile.model_dump())
    
    return result