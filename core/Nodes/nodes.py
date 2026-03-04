from services.parser.pdf_reader_n_clearner import pdf_reader
from agents.Job_ranker import start_career_optimization
from services.scraper.Job_scraper import fetch_jobs
from agents.Resume_extraction_agent import Resume_extaction
from agents.resume_rewrite_agent import resume_rewrite
from agents.suggested_Job_formating import suggested_Job_formating
from agents.human_rewritter_agent import human_rewritter_agent
from core.Nodes.Conditions import ingestion_condition, skill_extraction_condition, job_search_condition, critic_resume_rewrite_condition
from core.Nodes.GraphState import GraphState

from langgraph.graph import StateGraph,START,END

graph = StateGraph(GraphState)


graph.add_node('pdf_reader', pdf_reader)
graph.add_node('Resume_extaction', Resume_extaction)
graph.add_node('fetch_jobs', fetch_jobs)
graph.add_node('start_career_optimization', start_career_optimization)
graph.add_node('suggested_Job_formating', suggested_Job_formating)
graph.add_node('resume_rewrite', resume_rewrite)
graph.add_node('human_rewritter_agent', human_rewritter_agent)

graph.add_edge(START, 'pdf_reader')
graph.add_edge('pdf_reader', 'Resume_extaction')

graph.add_conditional_edges('Resume_extaction', ingestion_condition, {
    "passed": 'suggested_Job_formating',
    "retry": 'Resume_extaction',
    "failed": END
})

graph.add_conditional_edges('suggested_Job_formating', skill_extraction_condition, {
    "passed": 'fetch_jobs', 
    "retry": 'suggested_Job_formating',
    "failed": END
})

# graph.add_conditional_edges('suggested_Job_formating',job_search_condition,{
#     "passed": 'fetch_jobs',
#     "retry": 'suggested_Job_formating'

#     # how do we pass in the feedback from the job search condition to the suggested job formatting agent to suggest new the job search results ?
# })

graph.add_conditional_edges('fetch_jobs',critic_resume_rewrite_condition,{
    "Procced": 'resume_rewrite',
    "retry": 'fetch_jobs'

    # how do we pass in the feedback from the critic condition to the resume rewrite agent to improve the resume rewrite results ?
})

graph.add_edge('resume_rewrite','human_rewritter_agent')


graph.add_edge('human_rewritter_agent',END)

app = graph.compile()


def test_graph_with_data():
    """Test the graph with sample data and real-time state tracking"""
    
    # Initial input
    test_input = {
        "file": "resumes/Alex_Rivers.pdf"
    }

    try:
        print("▶️  Running graph with streaming...\n")
        print("=" * 50)
        
        # Using .stream to watch the state move between nodes
        # 'stream_mode="updates"' shows only what changed in each node
        for event in app.stream(test_input, stream_mode="updates"):
            for node_name, state_update in event.items():
                print(f"📍 NODE COMPLETED: {node_name}")
                
                # Check if raw_resume was updated in this step
                
                if state_update and isinstance(state_update, dict) and "raw_resume" in state_update:
                    text = state_update["raw_resume"]
                    preview = text[:100].replace('\n', ' ') if text else "None"
                    print(f"✅ raw_resume updated: '{preview}...'")
                
                # Check if parsed_skills was updated
                if "parsed_skills" in state_update:
                    print(f"✅ parsed_skills updated: {list(state_update['parsed_skills'].keys()) if state_update['parsed_skills'] else 'Empty'}")

                # Print the full update for this specific node
                print(f"📊 Full update from this node: {state_update}")
                print("-" * 50)
        
        # Final output after all nodes finish
        # Note: In stream mode, the last event contains the final state, 
        # but to keep it simple, we'll just acknowledge completion here.
        print("\n" + "=" * 80)
        print("✅ GRAPH EXECUTION FINISHED")
        print("=" * 80)
        
    except Exception as e:
        print("\n" + "=" * 80)
        print(f"❌ ERROR during graph execution")
        print("=" * 80)
        print(f"\n{type(e).__name__}: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return None

# Run the test
test_graph_with_data()