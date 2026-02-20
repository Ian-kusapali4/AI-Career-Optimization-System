from agents.Job_ranker import start_career_optimization
from agents.Career_Path_Agent import generate_career_suggestions
from agents.Resume_extraction_agent import Resume_extaction
from agents.resume_rewrite_agent import resume_rewrite
from agents.suggested_Job_formating import suggested_Job_formating
from core.Nodes.GraphState import GraphState

from langgraph.graph import StateGraph,START,END

graph = StateGraph(GraphState)

graph.add_node('start_career_optimization',start_career_optimization)
graph.add_node('generate_career_suggestions',generate_career_suggestions)
graph.add_node('Resume_extaction',Resume_extaction)
graph.add_node('resume_rewrite',resume_rewrite)
graph.add_node('suggested_Job_formating',suggested_Job_formating)

graph.add_edge(START,'Resume_extaction')
graph.add_edge('resume_rewrite',END)