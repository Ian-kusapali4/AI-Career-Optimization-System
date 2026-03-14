from core.Nodes.GraphState import GraphState

def select_job_details(state: GraphState):
    """
    Acts as a data filter. It takes the full list and returns 
    ONLY the chosen job, clearing the rest of the listings.
    """
    target_id = state.selected_job_id
    all_listings = state.job_listings.get("results", [])

    try:
        # Assuming your CLI/UI passed an integer index as selected_job_id
        selected_index = int(target_id)
        chosen_job = all_listings[selected_index]
    except (ValueError, IndexError, TypeError):
        # Fallback if selection fails
        return {"error_message": "Invalid job selection. Please try again."}

    print(f"🎯 Job Selected: {chosen_job['title']} at {chosen_job['company']}")

    return {
        # ✂️ THE PRUNING STEP:
        "job_listings": None,           # Wipe the 60 jobs from memory
        #"raw_resume": None,             # Wipe the raw text (we have CandidateProfile)
        "target_job_description": chosen_job['description'], # Store just the target description
        "selected_job_id": str(target_id) 
    }