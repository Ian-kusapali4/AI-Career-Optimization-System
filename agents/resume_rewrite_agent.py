import json
from langchain_ollama import ChatOllama
from services.parser.yaml_parser import yaml_extraction
from core.Nodes.GraphState import GraphState


config = yaml_extraction('config.yaml')
ranking_config = yaml_extraction('jobrating.yaml') 

model_name = config['model_settings']['name'] if config else "llama3"
my_model = ChatOllama(model=model_name)

def resume_rewrite(graph_state: GraphState):
    """
    Simplified for Streamlit: 
    Takes the specific job dictionary and the resume text.
    """
    resume_text = graph_state.raw_resume
    try:
        rewrite_prompt = ranking_config['career_architect']['rewrite_template'].format(
            role=ranking_config['career_architect']['role'],
            selected_job=json.dumps(graph_state.selected_job_id),
            resume=resume_text
        )
    except KeyError as e:
        return f"Error: Missing template key {e} in jobrating.yaml"

    print("\n--- AI IS REWRITING RESUME ---")
    final_resume = my_model.invoke(rewrite_prompt)
    
    return {'rewritten_resume': final_resume.content}

if __name__=="__main__":
    print("Test mode: Rewrite agent loaded.")