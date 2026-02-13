
from agents.Resume_extraction_agent import resume_data 
from agents.Career_Path_Agent import generate_career_suggestions
from services.parser.yaml_parser import yaml_extraction

#Loops throught the suggested jobs and separates the job title and reasoning 

def suggested_Job_formating():
    
    print("Step 1: Auditing Resume...")
    profile = resume_data() 
    config = yaml_extraction('Jobalocation.yaml')
    
    career_path_obj = generate_career_suggestions(profile, config)
    
    just_titles = [item.title for item in career_path_obj.suggestions]

   
    print("\n" + "="*40)
    print("LIST OF TARGET TITLES FOR SCRAPER:")
    print("="*40)
    for title in just_titles:
        print(f"✅ {title}")
    
    return just_titles

if __name__ == "__main__":
    final_titles = suggested_Job_formating()
    print(final_titles)