import pandas as pd
import time
import random
from jobspy import scrape_jobs
from core.Nodes.GraphState import GraphState

def fetch_jobs(state: GraphState):
    # 1. Gather suggestions and local location
    suggestions = state.search_queries.get("suggestions", [])
    
    # We use 'jobGeo' because your logs showed extracted location there
    location = state.CandidateProfile.get("jobGeo", "Remote") 
    
    # Create the list of titles to search
    search_titles = [s.get("title") for s in suggestions] if suggestions else [state.CandidateProfile.get("jobTitle", "Software Engineer")]
    
    print(f"🚀 AI suggested titles for search: {search_titles}")

    all_scraped_jobs = []

    # 2. LOOP through each title with Human-like delays
    for index, title in enumerate(search_titles):
        # Only sleep if it's NOT the first search
        if index > 0:
            delay = random.uniform(2.5, 5.5) # Random sleep between 2.5 and 5.5 seconds
            print(f"😴 Mimicking human behavior... waiting {delay:.2f}s before next search.")
            time.sleep(delay)

        print(f"🔍 Searching for: '{title}' in '{location}'...")
        
        try:
            jobs_df = scrape_jobs(
                site_name=["indeed", "linkedin", "zip_recruiter", "google"],
                search_term=title,
                location=location,
                results_wanted=10, 
                hours_old=72,
                country_indeed='USA',
                linkedin_fetch_description=True 
            )

            if not jobs_df.empty:
                for _, row in jobs_df.iterrows():
                    job_object = {
                        "title": str(row.get('title', 'N/A')),
                        "company": str(row.get('company', 'N/A')),
                        "url": str(row.get('job_url', '')),
                        "description": str(row.get('description', 'No description available.')),
                        "source": str(row.get('site', 'Unknown')),
                        "location": str(row.get('location', 'N/A')),
                        "match_score": 0 
                    }
                    all_scraped_jobs.append(job_object)
                    
        except Exception as e:
            print(f"⚠️ JobSpy failed for '{title}': {e}")
            continue 

    # 3. Deduplicate based on Job URL
    seen_urls = set()
    unique_jobs = []
    for job in all_scraped_jobs:
        if job['url'] not in seen_urls:
            unique_jobs.append(job)
            seen_urls.add(job['url'])

    print(f"✅ Total Unique Jobs Found: {len(unique_jobs)}")

    return {
        "job_listings": {"results": unique_jobs, "total_found": len(unique_jobs)},
        "retry_count": state.retry_count + 1
    }