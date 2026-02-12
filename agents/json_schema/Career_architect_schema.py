from pydantic import BaseModel, Field
from typing import List

class SuggestedRole(BaseModel):
    title: str = Field(description="The suggested job title.")
    reason: str = Field(description="Why this title fits the candidate's profile.")

class CareerPath(BaseModel):
    suggestions: List[SuggestedRole]