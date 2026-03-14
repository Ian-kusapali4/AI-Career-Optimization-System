import json
from langchain_ollama import ChatOllama
from services.parser.yaml_parser import yaml_extraction
from core.Nodes.GraphState import GraphState
from core.model_factory import get_model



my_model = get_model()
ranking_config = yaml_extraction('jobrating.yaml')

def resume_rewrite(graph_state: GraphState):
    # 1. Use the pruned data, not the ID
    # In our Selection node, we saved the target job description to final_resume
    target_job_description = graph_state.final_resume 
    resume_text = graph_state.raw_resume # Or CandidateProfile if you pruned raw_resume
    
    try:
        rewrite_prompt = ranking_config['career_architect']['rewrite_template'].format(
            role=ranking_config['career_architect']['role'],
            # ✅ PASS THE FULL TEXT, NOT THE ID
            selected_job=target_job_description, 
            resume=resume_text
        )
    except KeyError as e:
        return {"error_message": f"Error: Missing template key {e}"}

    print("\n--- AI IS REWRITING RESUME ---")
    final_resume = my_model.invoke(rewrite_prompt)
    
    return {'rewritten_resume': final_resume.content}