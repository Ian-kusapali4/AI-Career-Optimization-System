
from agents.Resume_extraction_agent import resume_data 
from agents.Career_Path_Agent import generate_career_suggestions
from services.parser.yaml_parser import yaml_extraction


def suggested_Job_formating(text_input):
    
    print("Step 1: Auditing Resume...")

    profile = resume_data(text_input) 

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
    # Local testing logic
    test_text = "Sample resume content for testing"
    final_titles = suggested_Job_formating(test_text)
    print(final_titles)