from pydantic import BaseModel, Field
from typing import List, Optional

#the data being extracted from the resume after assessment 
class CandidateProfile(BaseModel):
    
    jobTitle: str = Field(description="The professional title the candidate is currently holding or targeting.")
    companyName: Optional[str] = Field(description="The candidate's current or most recent employer.")
    
    
    jobIndustry: List[str] = Field(description="List of industries the candidate has experience in (e.g., Programming, Marketing).")
    jobType: List[str] = Field(description="Preferred work types, e.g., 'Full-Time', 'Freelance', 'Contract'.")
    
    
    jobGeo: str = Field(default="Remote",description="The candidate's current location (Country or City).")
    jobLevel: str = Field(default="Junior",description="Seniority level: 'Junior', 'Midweight', 'Senior', or 'Lead'.")
    
    
    skills: List[str] = Field(description="Technical skills found in the resume (e.g., Python, Pytest, Docker, Rust).")
    years_of_experience: int = Field(description="Total number of years in software development or relevant fields.")

    
    jobExcerpt: str = Field(description="A 2-3 sentence professional summary highlighting the candidate's best qualifications.")