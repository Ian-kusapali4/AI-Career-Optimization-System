
import json
from langchain_ollama import ChatOllama
from services.parser.yaml_parser import yaml_extraction


from agents.Resume_extraction_agent import resume_data 
from services.scraper.Job_scraper import fetch_jobs
from agents.suggested_Job_formating import suggested_Job_formating

#takes the resume, found jobs and ranks them after approvel the resume is rewriten for the job

config = yaml_extraction('config.yaml')
if config is None:
    print("Critical Error: Configuration could not be loaded. Exiting.")
    exit(1) 
model_name = config['model_settings']['name']

my_model = ChatOllama(model=model_name)

def start_career_optimization(resume_text, job_tags, config):

    current_tag = job_tags[0] if isinstance(job_tags, list) else job_tags
    jobs = fetch_jobs(current_tag)
    
    if not jobs:
        print("No jobs found to rank.")
        return

   
    scoring_prompt = config['career_architect']['scoring_template'].format(
        role=config['career_architect']['role'],
        resume=resume_text,
        jobs=json.dumps(jobs)
    )
    
    print("AI is scoring jobs...")
    
    ai_response = my_model.invoke(scoring_prompt)
    
    
    try:
        scored_results = json.loads(ai_response.content)
    except:
        print("AI didn't return perfect JSON, using fallback parser...")
       
        return

    
    for i, result in enumerate(scored_results):
        job = jobs[result['job_index']]
        print(f"\n[{i}] Score: {result['score']}/10 - {job['title']}")
        print(f"Reason: {result['reason']}")

    choice = int(input("\nEnter the index of the job you want to rewrite for: "))
    
   
    selected_job = jobs[scored_results[choice]['job_index']]
    rewrite_prompt = config['career_architect']['rewrite_template'].format(
        role=config['career_architect']['role'],
        selected_job=json.dumps(selected_job),
        resume=resume_text
    )
    
    print("\n--- REWRITING RESUME ---")
    final_resume = my_model.invoke(rewrite_prompt)
    print(final_resume.content)
    return scored_results,choice,jobs
    


if __name__ == "__main__":
    resume = resume_data()
    search_tags = suggested_Job_formating() 
    configer = yaml_extraction('jobrating.yaml')
    
    if configer:
        start_career_optimization(resume, search_tags, configer)