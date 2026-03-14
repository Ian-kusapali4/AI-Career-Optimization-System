from typing import List
from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class GraphState(BaseModel):
    
    # 1. Inputs
    file: str
    raw_resume: Optional[str] = None

    # 2. Extracted data
    CandidateProfile: Optional[Dict] = None
    

    #3. Discovery Data
    title_suggestions: Optional[List[Dict]] = None
    search_queries: Optional[Dict] = None
    job_listings: Optional[Dict] = None

     
     #4. Final Outputs
    selected_job_id: Optional[str] = None
    rewritten_resume: Optional[str] = None
    final_resume: Optional[str] = None
    target_job_description: Optional[str] = None
    
    # 5. ORCHESTRATION
    retry_count: int = 0
    ingestion_retries: int = 0
    search_retries: int = 0
    error_message: Optional[str] = None

    # 6. Feedback and Evaluation
    feedback: Optional[str] = None
    feedback_score: Optional[int] = None
    