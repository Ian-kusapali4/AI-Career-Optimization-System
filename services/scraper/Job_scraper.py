import requests
import urllib.parse
import re
from core.Nodes.GraphState import GraphState

def fetch_jobs(query, limit=20):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
   
    sources = [
        {
            "name": "Jobicy",
            "url": f"https://jobicy.com/api/v2/remote-jobs?tag={query}",
            "root": "jobs",           
            "map": {
                "title": "jobTitle", 
                "desc": "jobDescription",
                "company": "companyName",
                "url": "url"
            }
        },
        {
            "name": "Arbeitnow",
            "url": f"https://www.arbeitnow.com/api/job-board-api?search={query}",
            "root": "data",           
            "map": {
                "title": "title", 
                "desc": "description",
                "company": "company_name", # Arbeitnow specific key
                "url": "url"
            }
        }
    ]

    all_jobs = []

    for source in sources:
        try:
            print(f"[Scraper] Requesting {source['name']}...")
            response = requests.get(source['url'], headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            raw_jobs = data.get(source['root'], [])
            
            
            for item in raw_jobs[:limit]:
               
                raw_desc = item.get(source['map']['desc'], "")
                clean_desc = re.sub(r'<[^>]*>', '', raw_desc) 
                
                job_object = {
                    "title": item.get(source['map']['title']),
                    "company": item.get(source['map']['company'], "N/A"),
                    "url": item.get(source['map']['url']),
                    "description": clean_desc.strip(),
                    "source": source['name']
                }
                all_jobs.append(job_object)
            
            print(f"  > Collected {len(all_jobs)} jobs (limited to {limit}) from {source['name']}")

        except Exception as err:
            print(f"  ! Error fetching from {source['name']}: {err}")

    return {"job_listings": all_jobs}

if __name__ == "__main__":
   
    search_tags = ["python developer"] 
    
    total_found = 0

    for tag in search_tags:

        formatted_query = urllib.parse.quote(tag)
        found_jobs = fetch_jobs(formatted_query)
        total_found += len(found_jobs)

    print(f"\n--- SCRAPING COMPLETE ---")
    print(f"Total unique job objects ready for AI analysis: {total_found}")
    print(tag)