
from core.Nodes.GraphState import GraphState
from agents.Career_Path_Agent import generate_career_suggestions


def suggested_Job_formating(state: GraphState):
    print("Step: Generating Career Suggestions...")
    
    # Check if state is a dict (common in LangGraph streaming) or an object
    if isinstance(state, dict):
        # If it's a dict, we access keys with .get()
        parsed_skills = state.get('parsed_skills', {})
    else:
        parsed_skills = state.parsed_skills
    profile = {
        'jobTitle': parsed_skills.get('jobTitle', 'Not Specified'),
        'companyName': parsed_skills.get('companyName', 'Not Specified'),
        'jobIndustry': parsed_skills.get('jobIndustry', 'Not Specified'),
        'jobLevel': parsed_skills.get('jobLevel', 'Not Specified'),       
        'skills': parsed_skills.get('skills', []),
        'years_of_experience': parsed_skills.get('years_of_experience', 0),
        'jobExcerpt': parsed_skills.get('jobExcerpt', 'No summary available')
    }

    result = generate_career_suggestions(profile)

    # Return the dictionary to update the GraphState
    return {
        "Profile": profile, 
        "search_queries": result.model_dump()
    }
    # just_titles = [item.title for item in career_path_obj.suggestions]

    # print("\n" + "="*40)
    # print("LIST OF TARGET TITLES FOR SCRAPER:")
    # print("="*40)
    # for title in just_titles:
    #     print(f"✅ {title}")
    
    # return {"search_tags": just_titles}

if __name__ == "__main__":
    # Local testing logic
    test_text = "Sample resume content for testing"
    final_titles = suggested_Job_formating(test_text)
    print(final_titles)