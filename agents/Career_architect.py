
from agents.auditor_logic import resume_data 
from agents.architect import generate_career_suggestions
from services.parser.yaml_parser import yaml_extraction


def main():
    # --- 1. AUDIT ---
    print("Step 1: Auditing Resume...")
    profile = resume_data() 
    config = yaml_extraction('Jobalocation.yaml')
    
    career_path_obj = generate_career_suggestions(profile, config)
    
    just_titles = [item.title for item in career_path_obj.suggestions]

    # --- 5. OUTPUT ---
    print("\n" + "="*40)
    print("LIST OF TARGET TITLES FOR SCRAPER:")
    print("="*40)
    for title in just_titles:
        print(f"✅ {title}")
    
    return just_titles

if __name__ == "__main__":
    final_titles = main()
    print(final_titles)