import json
from langchain_ollama import ChatOllama
from services.parser.yaml_parser import yaml_extraction
from Core.Unifiedstate import IndigoMasterState 
from Core.model_factory import get_model

# This agent is responsible for rewriting the resume based on the job description and the candidate's profile. It takes the original resume, the target job decription

my_model = get_model()
ranking_config = yaml_extraction('jobrating.yaml')

def resume_rewrite(graph_state: IndigoMasterState):
    """This agent is responsible for rewriting the resume based on the job description and the candidate's profile. It takes the original resume, the target job description"""
    
    target_job_description = graph_state.get("final_resume") 
    resume_text = graph_state.get("raw_resume") 
    
    try:
        rewrite_prompt = ranking_config['career_architect']['rewrite_template'].format(
            role=ranking_config['career_architect']['role'],
          
            selected_job=target_job_description, 
            resume=resume_text
        )
    except KeyError as e:
        return {"error_message": f"Error: Missing template key {e}"}

    print("\n--- AI IS REWRITING RESUME ---")
    final_resume = my_model.invoke(rewrite_prompt)
    
    return {'resume_suggestions': final_resume.content}