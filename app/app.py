import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.Nodes.nodes import nodes 
from core.Nodes.GraphState import GraphState

# --- 1. Page Config ---
st.set_page_config(page_title="Indigo", layout="wide", page_icon="🚀")

if "graph_app" not in st.session_state:
    st.session_state.graph_app = nodes()
    st.session_state.thread_id = "streamlit_session_1"

config = {"configurable": {"thread_id": st.session_state.thread_id}}

st.title("🚀 Indigo ai job app")
st.subheader("AI-Powered Resume Tailoring & Job Matching")


with st.sidebar:
    st.header("1. Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF resume", type="pdf")
    
    if uploaded_file:
        temp_path = os.path.join("temp_resume.pdf")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Resume Uploaded!")


if uploaded_file:
    current_state = st.session_state.graph_app.get_state(config)
    values = current_state.values
    
   
    has_final_resume = values.get("rewritten_resume") is not None
    is_interrupted = len(current_state.next) > 0 and "__interrupt__" in str(current_state.next)
    if values is not None:
        job_listings_data = values.get("job_listings") or {}
        job_results = job_listings_data.get("results", [])
    else:
        job_results = []
        st.error("📡 The Graph returned an empty state. Ollama might have timed out.")
    has_jobs = len(job_results) > 0

  
    if has_final_resume:
        st.balloons()
        st.success("✨ Your human-centric resume is ready!")
        
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("📋 Extracted Profile")
            st.json(values.get("CandidateProfile", {}))
            
        with col_right:
            st.subheader("✍️ Tailored Resume")
            st.markdown(values["rewritten_resume"])
            
            st.download_button(
                label="📥 Download as Markdown",
                data=values["rewritten_resume"],
                file_name="tailored_resume.md",
                mime="text/markdown",
                use_container_width=True
            )
            
        if st.button("🔄 Start New Analysis", use_container_width=True):
            st.session_state.clear()
            st.rerun()


    elif is_interrupted or has_jobs:
        if not has_jobs:
            st.error("🕵️ No jobs found for your specific titles.")
            st.info("The AI suggested very specific roles that aren't currently listed on Jobicy/Arbeitnow.")
            if st.button("🔄 Try Broad Search"):
                
                st.session_state.graph_app.update_state(config, {"search_queries": {"suggestions": [{"title": "Administrative", "reason": "Broad search fallback"}]}})
                st.rerun()
        else:
         
            st.header(" AI Career Insights")
            suggestions = values.get("search_queries", {}).get("suggestions", [])
            
            if suggestions:
                cols = st.columns(len(suggestions))
                for i, sug in enumerate(suggestions):
                    with cols[i]:
                        with st.expander(f"📌 {sug['title']}", expanded=True):
                            st.caption("Strategic Reason:")
                            st.write(sug['reason'])
            st.divider()

          
            st.header("🔍 Matching Job Openings")
            for i, job in enumerate(job_results):
                with st.container(border=True):
                    col_info, col_score, col_action = st.columns([3, 1, 1])
                    
                    with col_info:
                        st.subheader(job['title'])
                        st.write(f"🏢 **{job['company']}** | 📍 {job.get('source', 'Web Source')}")
                        with st.expander("📖 View Full Description"):
                            st.write(job.get('description', "No description provided."))
                    
                    
                    with col_action:
                        st.link_button("🔗 Apply Now", job['url'], use_container_width=True)
                        
                        if st.button("🚀 Tailor Resume", key=f"btn_{i}", use_container_width=True):
                            with st.spinner("Pruning data and generating rewrite..."):
                                st.session_state.graph_app.update_state(config, {"selected_job_id": str(i)})
                                for event in st.session_state.graph_app.stream(None, config, stream_mode="updates"):
                                    st.write(f"✔️ {list(event.keys())[0]} finished.")
                                st.rerun()

    # STAGE 1: Start Fresh (Resume uploaded, but no search started)
    else:
        st.info("👋 Resume uploaded. Ready to find matching jobs!")
        if st.button("🔍 Find Matching Jobs", type="primary"):
            with st.spinner("Analyzing Resume & Scraping Job Boards..."):
                initial_input = {"file": temp_path}
                for event in st.session_state.graph_app.stream(initial_input, config, stream_mode="updates"):
                    st.write(f"✔️ {list(event.keys())[0]} finished.")
                st.rerun()

else:
    st.info("Please upload a resume in the sidebar to begin.")