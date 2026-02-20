from typing import List
from pydantic import BaseModel, Field


class GraphState(BaseModel):
    raw_resume: str          # The starting text
    #user_notes: str          # User's extra context
    parsed_skills: dict      # Structured data (JSON)
    search_queries: List[str]# Google search strings
    query_search_response: bool #check if the user is happy with the search results or if we need to retry with different queries
    job_listings: List[dict] # Results from the web
    selected_job_id: str     # The user's choice
    final_resume: str        # The output