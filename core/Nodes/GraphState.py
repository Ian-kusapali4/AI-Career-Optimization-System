from typing import List
from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class GraphState(BaseModel):
    
    file: str
    raw_resume: Optional[str] = None
    parsed_skills: Optional[Dict] = None
    search_queries: Optional[Dict] = [] # Or default to an empty list
    Profile: Optional[Dict] = None
    title_suggestions: Optional[List[Dict]] = None
    query_search_response: Optional[bool] = None
    job_listings: List[Dict] = Field(default_factory=list) 
    selected_job_id: Optional[str] = None
    rewritten_resume: Optional[str] = None
    final_resume: Optional[str] = None
    feedback: Optional[str] = None
    