import json
from services.parser.yaml_parser import yaml_extraction
from services.scraper.Job_scraper import fetch_jobs
from core.model_factory import get_model
from core.Nodes.GraphState import GraphState


my_model = get_model()

def start_career_optimization( configer, status_widget=None,state:GraphState=None):
   
    queries = state.get('search_queries') or {}

    # Check if it's a list (old format) or a dict with 'suggestions' (new format)
    if isinstance(queries, list) and len(queries) > 0:
        current_tag = queries[0]
    elif isinstance(queries, dict):
        # Adjust this to match how you are storing suggestions (e.g., getting the first title)
        suggestions = queries.get("suggestions", [])
        current_tag = suggestions[0].get("title") if suggestions else "Remote"
    else:
        current_tag = "Remote" # Ultimate fallback
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