from Core.Unifiedstate import ElevateMasterState 
from services.parser.yaml_parser import yaml_extraction
from Core.model_factory import get_model

# This agent is responsible for rewriting the resume based on the user's writing style and the job requirements. It takes the original resume, the target job description, and a sample of the user's writing style as input, and produces a rewritten resume that is tailored to the job and matches the user's voice.
#still needs some work 

human_rewriter_config = yaml_extraction('Human_written_resume.yaml')

def human_rewritter_agent(graph_state: ElevateMasterState) -> str:
    my_model = get_model()
    """This agent is responsible for rewriting the resume based on the user's writing style and the job requirements. It takes the original resume, the target job description, and a sample of the user's writing style as input, and produces a rewritten resume that is tailored to the job and matches the user's voice."""
    
    human_rewriter_prompt = human_rewriter_config['Human_rewriter']['template'].format(
        role=human_rewriter_config['Human_rewriter']['role'],
        original_resume_text=graph_state.get("raw_resume"),
        target_job_description=graph_state.get("target_job_description")
    )
    
    resume_suggestions = my_model.invoke(human_rewriter_prompt)
    
    return {"final_resume": resume_suggestions.content}