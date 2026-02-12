import requests
import urllib.parse
# from agents.Career_architect import main # Keeping your original import structure

def fetch_jobs(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    # 1. Define your sources and how to map their data
    sources = [
        {
            "name": "Jobicy",
            "url": f"https://jobicy.com/api/v2/remote-jobs?tag={query}",
            "root": "jobs",           
            "map": {"title": "jobTitle", "desc": "jobDescription"}
        },
        {
            "name": "Arbeitnow",
            "url": f"https://www.arbeitnow.com/api/job-board-api?search={query}",
            "root": "data",           
            "map": {"title": "title", "desc": "description"}
        }
    ]

    all_jobs = []

    for source in sources:
        try:
            print(f"[Scraper] Requesting {source['name']}...")
            response = requests.get(source['url'], headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Get the list of jobs based on the 'root' key
            raw_jobs = data.get(source['root'], [])
            
            for item in raw_jobs:
                # Map the site-specific keys to our universal format
                job_object = {
                    "title": item.get(source['map']['title']),
                    "description": item.get(source['map']['desc']),
                    "source": source['name'] # Good for tracking where it came from
                }
                all_jobs.append(job_object)
            
            print(f"  > Found {len(raw_jobs)} jobs from {source['name']}")

        except Exception as err:
            print(f"  ! Error fetching from {source['name']}: {err}")

    return all_jobs

if __name__ == "__main__":
    # For testing, you can use a list or your main() import
    # search_tags = main() 
    search_tags = ["python developer"] 
    
    total_found = 0

    for tag in search_tags:
        # We use quote here, but individual URLs handle the query differently
        formatted_query = urllib.parse.quote(tag)
        found_jobs = fetch_jobs(formatted_query)
        total_found += len(found_jobs)

    print(f"\n--- SCRAPING COMPLETE ---")
    print(f"Total unique job objects ready for AI analysis: {total_found}")
    print(tag)