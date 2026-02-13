from pydantic import BaseModel, Field
from typing import List

#schema to manage the ai output after assessing the resume and creating job suggestions 

class SuggestedRole(BaseModel):
    title: str = Field(description="The suggested job title.")
    reason: str = Field(description="Why this title fits the candidate's profile.")

#list of suggested career paths after resume assessment 
class CareerPath(BaseModel):
    suggestions: List[SuggestedRole]