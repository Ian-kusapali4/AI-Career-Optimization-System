from core.Nodes.GraphState import GraphState


def ingestion_condition(graph_state: GraphState) -> bool:
    """
    Check if the graph state has the necessary information to proceed with ingestion.
    For example, we might require a raw resume to be present before we can extract skills.
    """
    count = 0
    if not graph_state.get('raw_resume'):
        while count < 3:
            print("retrying ingestion condition check...")
            count += 1
            return "retry"
        else:            
            print("Ingestion condition check failed after 3 attempts. Please provide a valid resume.")
        return "failed"
    return "passed"


def skill_extraction_condition(graph_state: GraphState) -> bool:
    """
    Check if the graph state has the necessary information to proceed with skill extraction.
    For example, we might require a parsed resume or raw resume to be present before we can extract skills.
    """
    count = 0
    if not graph_state.get('parsed_skills'):
        while count < 3:
            print("retrying skill extraction condition check...")
            count += 1
            return "retry"
        else:            
            print("Skill extraction condition check failed after 3 attempts. Please provide a valid resume.")
        return "failed"
    
    return "passed"


def job_search_condition(graph_state: GraphState) -> bool:


    """Checking if the user is happy with the job search results, if not we can retry the job search with different queries or parameters."""

    print(graph_state.get("search_queries","are you okay with these jobs ? or do you want to retry ?"))

    if graph_state.get("query_search_response") == True:

        return "passed"
    elif graph_state.get("query_search_response") == False:
        return "retry"
    
def  job_ranking_condition(graph_state: GraphState) -> bool:
    """checkes if the matched jobs are ranked above 70% match sore if not we dont display them to the user and ask if they want to retry with different search queries or parameters."""