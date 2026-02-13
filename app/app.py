import streamlit as st
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.Resume_extraction_agent import resume_data 
from agents.suggested_Job_formating import suggested_Job_formating 
from services.parser.yaml_parser import yaml_extraction
from services.parser.pdf_resume_reader import pdf_reader
from agents.Job_ranker import start_career_optimization
from agents.resume_rewrite_agent import resume_rewrite 


config = yaml_extraction('config.yaml')
ranking_config = yaml_extraction('jobrating.yaml')

st.set_page_config(page_title="AI Career Optimization System", layout="wide")

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = None
if 'suggested_titles' not in st.session_state:
    st.session_state.suggested_titles = None
if 'ranked_jobs' not in st.session_state:
    st.session_state.ranked_jobs = []
if 'selected_job' not in st.session_state:
    st.session_state.selected_job = None

st.title("🛡️ AI Career Optimization System")

# STEP 1: RESUME UPLOAD & AUDIT
if st.session_state.step == 1:
    st.header("Step 1: Resume Extraction & Audit")
    uploaded_file = st.file_uploader("Upload Target Resume", type="pdf")
    
    if uploaded_file and st.button("Audit Resume"):
        with st.spinner("🔍 Step 1: Auditing Resume..."):
            temp_path = "temp_upload.pdf"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            extracted_text = pdf_reader(temp_path)
            st.session_state.profile_data = resume_data(extracted_text) 
            st.session_state.suggested_titles = suggested_Job_formating(extracted_text)
            
            st.session_state.step = 2
            if os.path.exists(temp_path): os.remove(temp_path)
            st.rerun()

# STEP 2: JOB SEARCH & RANKING
if st.session_state.step == 2:
    st.header("Step 2: Live Job Matching")
    st.success("✅ Resume Audited. Suggested Roles identified.")
    
    titles = st.session_state.suggested_titles if st.session_state.suggested_titles else []
    st.write(f"**Target Titles:** {', '.join(titles)}")

    if st.button("Search & Rank Jobs"):
        with st.status("🚀 Running Career Optimization...", expanded=True) as status:
            results = start_career_optimization(
                resume_text=st.session_state.profile_data, 
                job_tags=st.session_state.suggested_titles,
                configer=ranking_config,
                status_widget=status 
            )
            status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
        
        st.session_state.ranked_jobs = results
        st.session_state.step = 3
        st.rerun()

# STEP 3: DISPLAY RANKED JOBS
if st.session_state.step == 3:
    st.header("Step 3: Top Matches for You")
    
    num_jobs = len(st.session_state.ranked_jobs)
    col_a, col_b = st.columns(2)
    col_a.metric("Total Jobs Evaluated", num_jobs)
    col_b.info("Check the match reasons and apply or tailor your resume.")

    if num_jobs == 0:
        st.warning("No matches found.")
        if st.button("Back to Search"):
            st.session_state.step = 1
            st.rerun()
    else:
        for idx, job in enumerate(st.session_state.ranked_jobs):
           
            job_details = job.get('full_job_data', {})
            job_url = job_details.get('url') or job_details.get('link') or job.get('url')
            
            with st.container(border=True):
                col_info, col_btn = st.columns([3, 1])
                
                with col_info:
                    st.subheader(f"{job.get('title', 'N/A')}")
                    st.write(f"🏢 **Company:** {job.get('company', 'N/A')}")
                    
                    score_val = float(job.get('score', 0))
                    st.progress(score_val / 10, text=f"Match Score: {score_val}/10")
                    st.info(f"**AI Reasoning:** {job.get('reason', 'N/A')}")

                with col_btn:
                    st.write("### Actions")
                    
                    if job_url:
                        st.link_button("🌐 Apply on Site", job_url, use_container_width=True)
                    else:
                        st.button("🔗 Link Missing", disabled=True, use_container_width=True)
                    
                   
                    if st.button(f"✍️ Tailor Resume", key=f"tailor_{idx}", use_container_width=True):
                        st.session_state.selected_job = job
                        st.session_state.step = 4
                        st.rerun()

                
                with st.expander("📖 View Full Job Description"):
                    description = job_details.get('description', "No description text found.")
                    st.markdown(description)

    if st.button("⬅️ Restart Search"):
        st.session_state.step = 1
        st.rerun()

# STEP 4: RESUME TAILORING
if st.session_state.step == 4:
    job_data = st.session_state.selected_job
    st.header(f"Step 4: Tailoring Resume for {job_data.get('title')}")
    st.subheader(f"Targeting: {job_data.get('company')}")
    
    with st.spinner("✍️ Writing tailored resume..."):
        final_text = resume_rewrite(
            resume_text=st.session_state.profile_data, 
            selected_job=job_data
        )
        st.text_area("Generated Tailored Content", final_text, height=500)
        
        
        st.download_button(
            label="💾 Download Tailored Resume",
            data=final_text,
            file_name=f"Resume_{job_data.get('company')}.txt",
            mime="text/plain"
        )

    if st.button("Back to Job List"):
        st.session_state.step = 3
        st.rerun()