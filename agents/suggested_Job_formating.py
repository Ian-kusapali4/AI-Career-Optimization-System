
from Core.Unifiedstate import ElevateMasterState 
from Job_match.agents.Career_Path_Agent import generate_career_suggestions

# this agent is reposible for extracting the candidates profile into a structure format, two schemas are being used to force format the model output into a specific format
def suggested_Job_formating(state: ElevateMasterState):
    print("Step: Generating Career Suggestions...")
    
    
    if isinstance(state, dict):
     
        CandidateProfile = state.get('CandidateProfile', {})
    else:
        CandidateProfile = state.CandidateProfile
    profile = {
        'jobTitle': CandidateProfile.get('jobTitle', 'Not Specified'),
        'companyName': CandidateProfile.get('companyName', 'Not Specified'),
        'jobIndustry': CandidateProfile.get('jobIndustry', 'Not Specified'),
        'jobLevel': CandidateProfile.get('jobLevel', 'Not Specified'),       
        'skills': CandidateProfile.get('skills', []),
        'years_of_experience': CandidateProfile.get('years_of_experience', 0),
        'jobExcerpt': CandidateProfile.get('jobExcerpt', 'No summary available')
    }

    result = generate_career_suggestions(profile)
    print(f"🔍 DEBUG: Profile extracted successfully: {profile} ❌ (CandidateProfile 2)")



    return {
        "CandidateProfile": profile, 
        "search_queries": result.model_dump()
    }


if __name__ == "__main__":

    test_text = "Sample resume content for testing"
    final_titles = suggested_Job_formating(test_text)
    print(final_titles)