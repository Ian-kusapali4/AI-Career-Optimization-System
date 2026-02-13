import json
from langchain_ollama import ChatOllama
from agents.Job_ranker import start_career_optimization
from agents.Resume_extraction_agent import resume_data
from services.parser.yaml_parser import yaml_extraction

config = yaml_extraction('config.yaml')
if config is None:
    print("Critical Error: Configuration could not be loaded. Exiting.")
    exit(1) 
model_name = config['model_settings']['name']

my_model = ChatOllama(model=model_name)

def resume_rewrite(scored_results,choice,jobs,resume_text):
    
    # 4. Rewrite Resume
    selected_job = jobs[scored_results[choice]['job_index']]
    rewrite_prompt = config['career_architect']['rewrite_template'].format(
        role=config['career_architect']['role'],
        selected_job=json.dumps(selected_job),
        resume=resume_text
    )
    
    print("\n--- REWRITING RESUME ---")
    final_resume = my_model.invoke(rewrite_prompt)
    print(final_resume.content)


if __name__=="__main__":
    resume = resume_data()
