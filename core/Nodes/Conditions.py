from core.Nodes.GraphState import GraphState
from services.parser.yaml_parser import yaml_extraction
from langchain_ollama import ChatOllama


config_base = yaml_extraction('config.yaml')
critic_config = yaml_extraction('critic_resume_rewrite.yaml')
model_name = config_base['model_settings']['name'] if config_base else "llama3"
my_model = ChatOllama(model=model_name)

def ingestion_condition(graph_state: GraphState) -> bool:
    """
    Check if the graph state has the necessary information to proceed with ingestion.
    For example, we might require a raw resume to be present before we can extract skills.
    """
    count = 0
    if not graph_state.raw_resume:
        while count < 3:
            print("retrying ingestion condition check...")
            count += 1
            return "retry"
        else:            
            print("Ingestion condition check failed after 3 attempts. Please provide a valid resume.")
        return "failed"
    return "passed"


def skill_extraction_condition(graph_state: GraphState):
    print(f"DEBUG: Profile exists: {graph_state.Profile is not None}")
    print(f"DEBUG: Search Queries exist: {graph_state.search_queries is not None}")

    if graph_state.Profile and graph_state.search_queries:
        print('--- CONDITION: PASSED ---')
        return "passed"


    if graph_state.parsed_skills:
        print("--- CONDITION: RETRYING ---")
        return "retry"
        
    print("--- CONDITION: FAILED ---")
    return "failed"

def job_search_condition(graph_state: GraphState) -> bool:


    """Checking if the user is happy with the job search results, if not we can retry the job search with different queries or parameters."""

    print(f"Search Queries: {graph_state.search_queries}")

    if graph_state.query_search_response == True:

        return "passed"
    elif graph_state.query_search_response == False:
        return "retry"
    
def critic_resume_rewrite_condition(graph_state: GraphState) -> bool:
    # """checkes the resume rewrite results, see if the response matches the job requirements, if not we can retry the resume rewrite with different prompts or parameters."""
    # try:
    #     critic_prompt = critic_config['Resume_critic']['template'].format(
    #         role=critic_config['Resume_critic']['role'],
    #         selected_job=graph_state.selected_job_id,
    #         final_resume=graph_state.final_resume
    #     )
    # except KeyError as e:
    #     print(f"YAML Key Error: {e}")
    #     return "failed"
    # print("\n--- AI IS CRITICIZING THE REWRITTEN RESUME ---")   
    # ai_response = my_model.invoke(critic_prompt)
    
    return "Procced"
