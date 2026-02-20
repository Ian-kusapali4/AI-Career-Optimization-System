from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from agents.json_schema.resume_extraction_schema import CandidateProfile
from langchain_core.output_parsers import PydanticOutputParser
from services.parser.yaml_parser import yaml_extraction

#Resume extraction agent, takes resume data and extracts the relevant fields



config_data = yaml_extraction('auditor.yaml')
config = yaml_extraction('config.yaml')
if config is None:
    print("Critical Error: Configuration could not be loaded. Exiting.")
    exit(1) 
model_name = config['model_settings']['name']

my_model = ChatOllama(model=model_name)


full_template = f"{config_data['system_message']}\n\n{config_data['user_template']}"
prompt_template = ChatPromptTemplate.from_template(full_template)
structured_llm = my_model.with_structured_output(CandidateProfile)

def Resume_extaction( prompt_template, resume_text, notes):
    parser = PydanticOutputParser(pydantic_object=CandidateProfile)
    format_instructions = parser.get_format_instructions()
    
    
    chain = prompt_template | structured_llm
    response = chain.invoke({
        "resume_text": resume_text,
        "user_notes": notes,
        "format_instructions": format_instructions
    })
    return response 

def resume_data(text_input):
    notes = ""
    result = Resume_extaction( prompt_template, text_input, notes)
    return result
