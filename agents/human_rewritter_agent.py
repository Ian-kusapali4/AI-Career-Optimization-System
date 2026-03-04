from core.Nodes.GraphState import GraphState
from services.parser.yaml_parser import yaml_extraction
from langchain_ollama import ChatOllama

config_base = yaml_extraction('config.yaml')
human_rewriter_config = yaml_extraction('Human_written_resume.yaml')
model_name = config_base['model_settings']['name'] if config_base else "llama3"
my_model = ChatOllama(model=model_name)

def human_rewritter_agent(graph_state: GraphState) -> str:
    """This agent is responsible for rewriting the resume based on the user's writing style and the job requirements. It takes the original resume, the target job description, and a sample of the user's writing style as input, and produces a rewritten resume that is tailored to the job and matches the user's voice."""
    
    human_rewriter_prompt = human_rewriter_config['Human_rewriter']['template'].format(
        role=human_rewriter_config['Human_rewriter']['role'],
        original_resume_text=graph_state.get("original_resume_text"),
        target_job_description=graph_state.get("target_job_description"),
        user_writing_sample=graph_state.get("user_writing_sample")
    )
    
    rewritten_resume = my_model.invoke(human_rewriter_prompt)
    
    return {"final_resume": rewritten_resume.content}