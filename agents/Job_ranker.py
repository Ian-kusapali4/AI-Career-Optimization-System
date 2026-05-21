import json
from services.parser.yaml_parser import yaml_extraction
from services.scraper.Job_scraper import fetch_jobs
from Core.model_factory import get_model
from Core.Unifiedstate import ElevateMasterState 

#this agent is currently not in use because of token useage, but we plan to use it in the future to rank jobs based on the candidate's profile and the job description. It will take the job listings fetched by the scraper and use an LLM to score and rank them based on relevance to the candidate's profile and the job requirements. 
#currntly exporing four options either we use rag to store the jobs found and then use the model to rank them since the context window will be smaller  or we use a hrd coded funtion to rank the jobs based on key factors like required skills, location, and company size. The third option is to use a more powerful model with a larger context window that can handle the full job descriptions without needing to summarize them first or maybe we can use a combination of all three approaches to optimize the ranking process while managing token usage effectively.



def start_career_optimization( configer, status_widget=None,state:ElevateMasterState=None):
    my_model = get_model()
    """This agent orchestrates the career optimization process. It takes the current graph state, extracts search queries, fetches relevant job listings, and then uses an LLM to score and rank these jobs based on the candidate's profile."""
    queries = state.get('search_queries') or {}

    
    if isinstance(queries, list) and len(queries) > 0:
        current_tag = queries[0]
    elif isinstance(queries, dict):
       
        suggestions = queries.get("suggestions", [])
        current_tag = suggestions[0].get("title") if suggestions else "Remote"
    else:
        current_tag = "Remote" # Default fallback if no queries are found
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