import json
from langchain_ollama import ChatOllama
from services.parser.yaml_parser import yaml_extraction
from services.scraper.Job_scraper import fetch_jobs
from core.Nodes.GraphState import GraphState


config_base = yaml_extraction('config.yaml')
model_name = config_base['model_settings']['name'] if config_base else "llama3"
my_model = ChatOllama(model=model_name)

def start_career_optimization( configer, status_widget=None,state:GraphState=None):
   
    current_tag = state['search_queries'][0] if isinstance(state['search_queries'], list) else state['search_queries']
    
    if status_widget:
        status_widget.write(f"🔍 Searching for: **{current_tag}**...")
    
    state['job_listings'] = fetch_jobs(current_tag, limit=20)['job_listings']

    if status_widget:
        status_widget.write(f"✅ Scraper found **{len(state['job_listings'])}** jobs total.")
        status_widget.write("🤖 AI is now scoring these jobs for your profile...")
   
    try:
        scoring_prompt = configer['career_architect']['scoring_template'].format(
            role=configer['career_architect']['role'],
            resume=state['job_listings'],
            jobs=json.dumps(state['job_listings'])
        )
    except KeyError as e:
        print(f"YAML Key Error: {e}")
        return []
    
   
    ai_response = my_model.invoke(scoring_prompt)
    
    try:
        content = ai_response.content.strip()
        
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
            
        scored_results = json.loads(content)
        valid_results = []
        
        
        for result in scored_results:
            idx = result.get('job_index')
            if idx is not None and 0 <= idx < len(state['job_listings']):
                result['title'] = state['job_listings'][idx].get('title', 'N/A')
                result['company'] = state['job_listings'][idx].get('company', 'N/A')
                result['full_job_data'] = state['job_listings'][idx]
                valid_results.append(result)
            else:
                print(f"⚠️ AI suggested index {idx}, but it's out of range. Skipping.")
            
        return valid_results
        
    except Exception as e:
        print(f"JSON Parsing Error: {e}")
        return []