import streamlit as st
import os
import time
import json
from datetime import datetime
from src.pipeline.rag_pipeline import RAGPipeline

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="The Civic Scribe | Executive Archive", layout="wide")

# --- 2. THEME STATE ---
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# --- 3. DYNAMIC DESIGN SYSTEM ---
primary_green = "#107C41"
gold_accent = "#FCD116" 

if st.session_state.theme == "Light":
    bg_color = "#F8F9FA"
    card_bg = "#FFFFFF"
    text_color = "#1F2937"
    border_color = "#E5E7EB"
    status_bg = "#E8EDF2"
else:
    bg_color = "#0F172A"
    card_bg = "#1E293B"
    text_color = "#F1F5F9"
    border_color = "#334155"
    status_bg = "#1E293B"

custom_css = f"""
<style>
.stApp {{ background-color: {bg_color}; color: {text_color}; }}
.top-bar-container {{
    background-color: {primary_green}; 
    padding: 20px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 5px solid #D4AF37; 
    margin: -6rem -5rem 2.5rem -5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    position: relative;
    height: 100px;
}}
.top-bar-title {{ color: white !important; margin: 0; font-family: 'Georgia', serif; font-size: 2.2rem; text-align: center; flex-grow: 1; }}
.coat-of-arms {{ height: 60px; }}
.executive-card {{ background-color: {card_bg}; border-radius: 8px; padding: 1.5rem; border-top: 4px solid {primary_green}; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 1.5rem; }}
.annex-title {{ color: {primary_green} !important; font-family: 'Georgia', serif !important; font-size: 1.8rem !important; border-bottom: 2px solid {primary_green} !important; }}
.status-box {{ background-color: {status_bg}; padding: 18px; border-radius: 6px; margin-bottom: 1.5rem; }}
.archive-card {{ background-color: {card_bg}; border-left: 6px solid {primary_green}; padding: 1rem; margin-bottom: 0.5rem; }}
.score-badge {{ background-color: #FFD700; color: #000; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: bold; }}
div[data-testid="stButton"] button {{ background-color: {primary_green} !important; color: white !important; }}
#MainMenu, footer, header {{visibility: hidden;}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- 4. TOP BANNER ---
t_col, _ = st.columns([1, 9])
with t_col:
    st.markdown('<div style="margin-top: -3.5rem; position: relative; z-index: 999;">', unsafe_allow_html=True)
    mode = st.toggle("Dark Mode", value=(st.session_state.theme == "Dark"))
    st.markdown('</div>', unsafe_allow_html=True)
    if mode != (st.session_state.theme == "Dark"):
        st.session_state.theme = "Dark" if mode else "Light"
        st.rerun()

st.markdown(f"""
<div class="top-bar-container">
    <h1 class="top-bar-title">THE CIVIC SCRIBE | Executive Archive</h1>
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Coat_of_arms_of_Ghana.svg/500px-Coat_of_arms_of_Ghana.svg.png" class="coat-of-arms">
</div>
""", unsafe_allow_html=True)

# --- 5. INITIALIZATION WITH CACHING ---
@st.cache_resource
def load_rag_pipeline():
    """
    Load the pre-computed index and initialize the pipeline.
    This replaces get_pipeline_v4 and uses pre-computed data to save RAM.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    pipeline = RAGPipeline(data_dir=data_dir)
    # This loads from .index and _chunks.json files
    pipeline.initialize_from_index()
    return pipeline

# Initialize Session State
if "active_briefing" not in st.session_state: st.session_state.active_briefing = None
if "telemetry" not in st.session_state: st.session_state.telemetry = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "suggestion_text" not in st.session_state: st.session_state.suggestion_text = ""

with st.status("Accessing Executive Archives...", expanded=False) as status:
    try:
        pipeline = load_rag_pipeline()
        status.update(label="Intelligence Systems Online", state="complete", expanded=False)
    except Exception as e:
        status.update(label="Initialization Failed", state="error", expanded=True)
        st.error(f"Error loading archives: {e}. Ensure you have run 'build_index.py' locally.")

# --- 6. MAIN CONTENT ---
col1, col2 = st.columns([2.5, 1], gap="large")

with col1:
    st.markdown('<h3 style="color: forestgreen; margin-bottom: 0;">Enter Inquiry Directive...</h3>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.1rem; color: #6B7280; margin-bottom: 1rem;">I am an AI Assistant to help you out.</p>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    
    sug_col1, sug_col2, sug_col3 = st.columns(3)
    with sug_col1:
        if st.button("📄 2025 Education Budget", use_container_width=True):
            st.session_state.suggestion_text = "Summarize the 2025 education budget."
            st.rerun()
    with sug_col2:
        if st.button("🇬🇭 2020 Election Results", use_container_width=True):
            st.session_state.suggestion_text = "Show 2020 election results by region."
            st.rerun()
    with sug_col3:
        if st.button("⚙️ Infrastructure Projects", use_container_width=True):
            st.session_state.suggestion_text = "Key 2025 infrastructure projects."
            st.rerun()
            
    query = st.text_input("Directive", value=st.session_state.suggestion_text, placeholder="Ask me anything", label_visibility="collapsed")
    
    if st.button("Process Executive Directive", use_container_width=True):
        if query:
            with st.status("Fetching Executive Data...", expanded=True) as status:
                now = datetime.now().strftime("%I:%M %p")
                current_logs = [{"dot": "#10B981", "time": now, "msg": "Secure server connection established."}]
                chunks, scores, final_prompt, stream_gen = pipeline.query_stream(query, top_k=4, chat_history=st.session_state.chat_history)
                current_logs.append({"dot": "#3B82F6", "time": now, "msg": "Scanning national archives..."})
                full_response = st.write_stream(stream_gen)
                status.update(label="Inquiry Processed", state="complete", expanded=False)

            st.session_state.active_briefing = {"query": query, "response": full_response}
            st.session_state.chat_history.append({"role": "user", "content": query})
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            st.session_state.telemetry = {"chunks": chunks, "scores": scores, "prompt": final_prompt, "trace_logs": current_logs}
            st.rerun()

    if st.button("New Directive", use_container_width=False):
        st.session_state.suggestion_text = ""
        st.session_state.chat_history = []
        st.session_state.active_briefing = None
        st.session_state.telemetry = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.active_briefing:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        st.markdown("## Latest Briefing Report")
        st.markdown(st.session_state.active_briefing['response'])
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<h3 class="annex-title">Evidentiary Annex</h3>', unsafe_allow_html=True)
    
    if not st.session_state.telemetry:
        st.markdown('<div class="status-box"><span class="status-text">Submit an inquiry directive to view archive retrieval logs and source evidence.</span></div>', unsafe_allow_html=True)
    else:
        for log in st.session_state.telemetry["trace_logs"]:
            st.markdown(f'<div style="font-size:0.8rem; padding: 3px 0;"><span style="color:{log["dot"]};">●</span> <strong>{log["time"]}:</strong> {log["msg"]}</div>', unsafe_allow_html=True)
        
        st.write("")
        st.markdown("<h4>Retrieved Archives</h4>", unsafe_allow_html=True)
        for i, chunk in enumerate(st.session_state.telemetry["chunks"]):
            score_data = st.session_state.telemetry["scores"].get(chunk['chunk_id'], {})
            score_val = score_data.get("final_score", 0.0) if isinstance(score_data, dict) else float(score_data)
            
            with st.expander(f"Archive {i+1}: {chunk['source']}", expanded=(i==0)):
                st.markdown(f"""
                <div class="archive-card">
                    <span class="score-badge">Score: {score_val:.2f}</span>
                    <div style="margin-top: 10px;">{chunk['text']}</div>
                </div>
                """, unsafe_allow_html=True)

        with st.expander("🔍 View LLM Payload"):
            st.code(st.session_state.telemetry["prompt"], language="markdown")
