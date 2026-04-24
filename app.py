import streamlit as st
import os
import time
from src.pipeline.rag_pipeline import RAGPipeline

# Must be the first Streamlit command
st.set_page_config(page_title="THE CIVIC SCRIBE", page_icon="🇬🇭", layout="wide")

# Custom CSS for Oman Ledger Overhaul
st.markdown("""
<style>
/* ==========================================================================
   1. IMPORTS & VARIABLES
   ========================================================================== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Merriweather:ital,wght@0,400;0,700;1,400&display=swap');

:root {
    /* Color Palette */
    --color-forest-green: #0B6623;
    --color-forest-green-hover: #084D1A;
    --color-gold: #FCD116;
    --color-cream: #FDFBF7;
    --color-charcoal: #333333;
    --color-grey-border: #E5E7EB;
    --color-grey-text: #4B5563;
    --color-white: #FFFFFF;
    
    /* New: Info & Log Colors */
    --color-info-bg: #E0E7FF;
    --color-info-text: #1E3A8A;

    /* Typography */
    --font-primary: 'Inter', sans-serif;
    --font-secondary: 'Merriweather', serif;
    
    /* Structural & Effects */
    --transition-speed: 0.25s;
    --border-radius: 6px;
    --shadow-soft: 0 4px 15px rgba(0, 0, 0, 0.05);
}

/* ==========================================================================
   2. STREAMLIT RESETS & GLOBAL STYLES
   ========================================================================== */
header, 
#MainMenu, 
footer {
    visibility: hidden;
    display: none;
}

.stApp {
    background-color: var(--color-cream);
    color: var(--color-charcoal);
    font-family: var(--font-primary);
    -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-secondary);
    color: var(--color-forest-green) !important;
}

/* ==========================================================================
   3. LAYOUT & CONTAINERS
   ========================================================================== */
/* Custom Top Bar */
.top-bar-container {
    background-color: var(--color-forest-green);
    border-bottom: 4px solid var(--color-gold);
    padding: 1.5rem 2.5rem;
    margin: -4rem -3rem 2rem -3rem; 
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.coat-of-arms {
    height: 70px; /* Adjust height to match the top bar */
    width: auto;
}

.top-bar-title {
    font-family: var(--font-secondary);
    color: var(--color-white) !important;
    font-size: clamp(1.4rem, 4vw, 1.75rem); 
    font-weight: 700;
    margin: 0;
}

/* Unified Card Layout for Both Columns
   Targets Streamlit's native columns to act as clean, matching cards
*/
[data-testid="column"] {
    background-color: var(--color-white) !important;
    border-top: 4px solid var(--color-forest-green) !important;
    border-radius: var(--border-radius) !important;
    padding: 1.5rem !important;
    box-shadow: var(--shadow-soft) !important;
    /* This removes the massive empty space below the elements */
    height: fit-content !important; 
    margin-bottom: 1rem;
}

/* Fix the double line under headers in the columns */
[data-testid="column"] h2, 
[data-testid="column"] h3 {
    border-bottom: 2px solid var(--color-forest-green) !important;
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem;
}
/* Hide Streamlit's native horizontal rule that causes the double line */
[data-testid="column"] hr {
    display: none !important;
}

/* ==========================================================================
   4. COMPONENTS (Inputs & Buttons)
   ========================================================================== */
/* Input Area Formatting */
.stTextInput input {
    background-color: var(--color-white) !important;
    color: var(--color-charcoal) !important;
    border: 1px solid #CCCCCC !important;
    border-radius: var(--border-radius) !important;
    font-family: var(--font-primary);
    font-size: 1rem;
    padding: 0.85rem 1rem;
    transition: box-shadow var(--transition-speed) ease;
}

.stTextInput input:focus {
    box-shadow: 0 0 0 3px rgba(252, 209, 22, 0.3) !important;
    border-color: var(--color-gold) !important;
    outline: none !important;
}

/* Executive Directive Button */
.stButton, 
div[data-testid="stButton"] {
    width: 100% !important;
    display: block !important;
}

.stButton button {
    width: 100% !important; /* Stretches horizontally */
    white-space: nowrap !important; /* Strictly prevents text clipping or wrapping */
    background-color: var(--color-forest-green, #0B6623) !important;
    color: var(--color-white, #FFFFFF) !important;
    border: none !important;
    border-radius: var(--border-radius, 6px) !important;
    font-family: var(--font-primary, 'Inter', sans-serif) !important;
    font-weight: 600 !important;
    padding: 0.75rem 1.75rem !important;
    box-shadow: 0 2px 4px rgba(11, 102, 35, 0.2) !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    transition: all 0.25s ease !important;
}

.stButton button:hover {
    background-color: var(--color-forest-green-hover, #084D1A) !important;
    color: var(--color-gold, #FCD116) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 8px rgba(11, 102, 35, 0.3) !important;
}

/* ==========================================================================
   5. NEW: EVIDENTIARY ANNEX LOG UI
   ========================================================================== */
.info-box {
    background-color: var(--color-info-bg);
    color: var(--color-info-text);
    padding: 1rem;
    border-radius: var(--border-radius);
    font-size: 0.9rem;
    font-family: var(--font-primary);
    margin-bottom: 1.5rem;
}

.log-container {
    border: 1px solid var(--color-grey-border);
    border-radius: var(--border-radius);
    background-color: var(--color-white);
    display: flex;
    flex-direction: column;
}

.log-entry {
    padding: 0.85rem 1rem;
    border-bottom: 1px solid var(--color-grey-border);
    font-size: 0.85rem;
    color: var(--color-charcoal);
    font-family: var(--font-primary);
    display: flex;
    align-items: center;
}

.log-entry:last-child {
    border-bottom: none;
}

/* New: Professional Status Indicators */
.status-dot {
    height: 8px;
    width: 8px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 10px;
}
.dot-green { background-color: #10B981; } /* Success/Ready */
.dot-yellow { background-color: #F59E0B; } /* Processing/Loading */
.dot-blue { background-color: #3B82F6; } /* Information */

/* ==========================================================================
   6. RESPONSIVE DESIGN (MOBILE)
   ========================================================================== */
@media screen and (max-width: 768px) {
    .top-bar-container {
        padding: 1.25rem;
        margin: -3rem -1.25rem 1.5rem -1.25rem; 
    }
    
    [data-testid="column"] {
        margin-top: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

top_bar_html = """
<div class="top-bar-container">
    <h1 class="top-bar-title">THE CIVIC SCRIBE | Executive Archive</h1>
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Coat_of_arms_of_Ghana.svg/500px-Coat_of_arms_of_Ghana.svg.png" class="coat-of-arms" alt="Ghana Coat of Arms">
</div>
"""

st.markdown(top_bar_html, unsafe_allow_html=True)

# Initialize Pipeline Cache (V4 - Final Sync)
@st.cache_resource
def get_pipeline_v4():
    pipeline = RAGPipeline(data_dir="data")
    pipeline.initialize(pdf_chunking_strategy="paragraph")
    return pipeline

# State Management for Single Briefing
if "active_briefing" not in st.session_state:
    st.session_state.active_briefing = None
if "telemetry" not in st.session_state:
    st.session_state.telemetry = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize Pipeline Behind the Scenes
pipeline = get_pipeline_v4()
if not pipeline.is_initialized:
    st.error("⚠️ Failed to initialize the pipeline. Please ensure the data files are in the `data/` directory.")
    st.stop()

# Layout: 65% Left, 35% Right
left_pane, right_pane = st.columns([6.5, 3.5], gap="large")

# ==============================
# LEFT PANE: The Briefing Area
# ==============================
with left_pane:
    
    with st.form("query_form"):
        st.markdown("<h4 style='margin-bottom: 0px;'>Enter Inquiry Directive...</h4>", unsafe_allow_html=True)
        query = st.text_input("Hidden Label", label_visibility="collapsed", placeholder=" Ask me about the 2025 Budget and Ghana Election...")
        
        # This button now spans the full width of the form container
        submit = st.form_submit_button("Process Executive Directive", use_container_width=True)

    # NEW: Clear Session / New Chat Option
    if st.button(" New Directive ", use_container_width=True, help="Clears all conversation history and resets the dashboard."):
        st.session_state.chat_history = []
        st.session_state.active_briefing = None
        st.session_state.telemetry = None
        st.rerun()

    # Processing Logic
    if submit and query:
        if not query.strip():
            st.warning("Please enter a valid directive.")
        else:
            with st.spinner("Compiling Executive Briefing..."):
                # Create a placeholder in the right pane for the live trace
                with right_pane:
                    trace_placeholder = st.empty()
                    
                    def update_trace(logs):
                        log_html = "<div class='log-container'>"
                        for l in logs:
                            log_html += f"<div class='log-entry'><span class='status-dot {l['dot']}'></span> <strong>{l['time']}:</strong> {l['msg']}</div>"
                        log_html += "</div>"
                        trace_placeholder.markdown(log_html, unsafe_allow_html=True)

                    current_logs = []
                    now = time.strftime("%I:%M %p")
                    
                    # Step 1: Connection
                    current_logs.append({"dot": "dot-green", "time": now, "msg": "Secure server connection established."})
                    update_trace(current_logs)
                    time.sleep(0.6)
                    
                    # Step 2: Parsing
                    current_logs.append({"dot": "dot-blue", "time": now, "msg": "Parsing directive for key civic parameters..."})
                    update_trace(current_logs)
                    
                    # Step 3: Run Actual Pipeline (Streaming)
                    start_time = time.time()
                    chunks, scores, final_prompt, stream_gen = pipeline.query_stream(
                        query, 
                        top_k=4, 
                        chat_history=st.session_state.chat_history
                    )
                    end_time = time.time()
                    
                    # Step 4: Scan (Simulated after query is fast)
                    current_logs.append({"dot": "dot-yellow", "time": now, "msg": "Scanning national electoral archives..."})
                    update_trace(current_logs)
                    time.sleep(0.5)
                    
                    # Step 5: Success
                    count = len(chunks)
                    current_logs.append({"dot": "dot-green", "time": now, "msg": f"{count} relevant archive(s) retrieved successfully."})
                    update_trace(current_logs)

            # --- Generation & Display (Streaming) ---
            st.markdown("## Briefing Report")
            st.caption(f"**Directive:** {query}")
            
            # Display the streaming response
            full_response = st.write_stream(stream_gen)
                
            # Update Session State
            st.session_state.active_briefing = {
                "query": query,
                "response": full_response
            }
            # Append to history
            st.session_state.chat_history.append({"role": "user", "content": query})
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            
            st.session_state.telemetry = {
                "chunks": chunks,
                "scores": scores,
                "prompt": final_prompt,
                "time": f"{end_time - start_time:.2f}s",
                "trace_logs": current_logs
            }
            # Rerun to ensure state is cleanly synced
            st.rerun()

    # Display Active Briefing (Persisted)
    if st.session_state.active_briefing:
        st.markdown("## Latest Briefing Report")
        st.caption(f"**Directive:** {st.session_state.active_briefing['query']}")
        st.markdown(st.session_state.active_briefing['response'])
        st.markdown("---")

    # Display Conversation History
    if st.session_state.chat_history:
        with st.expander("View Full Briefing History", expanded=False):
            # Show history in reverse order (newest first)
            for msg in reversed(st.session_state.chat_history[:-2]): # Skip the latest one shown above
                role_label = "EXECUTIVE DIRECTIVE" if msg["role"] == "user" else "SCRIBE RESPONSE"
                st.markdown(f"**{role_label}:**")
                st.markdown(msg["content"])
                st.markdown("---")

# ==============================
# RIGHT PANE: Evidentiary Annex
# ==============================
with right_pane:
    st.markdown("### Evidentiary Annex")
    st.markdown("<hr style='border-top: 2px solid #0B6623; margin-top: 0px;'/>", unsafe_allow_html=True)
    
    if st.session_state.telemetry and st.session_state.telemetry.get("chunks"):
        # ACTIVE STATE: Real-time execution trace
        trace_logs = st.session_state.telemetry.get("trace_logs", [])
        active_logs_html = "<div class='log-container'>"
        for l in trace_logs:
            active_logs_html += f"<div class='log-entry'><span class='status-dot {l['dot']}'></span> <strong>{l['time']}:</strong> {l['msg']}</div>"
        active_logs_html += "</div>"
        
        st.markdown(active_logs_html, unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # Section 1: Retrieved Archives
        st.markdown("#### Retrieved Archives")
        
        for idx, chunk in enumerate(st.session_state.telemetry["chunks"]):
            cid = chunk.get("chunk_id")
            source = chunk.get("source")
            scores = st.session_state.telemetry["scores"].get(cid, {})
            final_score = scores.get("final_score", 0)
            
            # Creating a professional label for the accordion
            label = f"[{idx+1}] {source} (Score: {final_score:.2f})"
            
            with st.expander(label):
                st.markdown(f"""
                <div style='padding: 10px; border-left: 4px solid var(--color-forest-green); background-color: var(--color-cream);'>
                    <div style='color: var(--color-grey-text); font-size: 0.9rem; line-height: 1.6;'>
                        {chunk.get('text')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
        # Section 2: Telemetry (Prompt)
        st.markdown("<br/>", unsafe_allow_html=True)
        with st.expander("View LLM Payload"):
            st.code(st.session_state.telemetry["prompt"], language="markdown")
            
    else:
        # STANDBY STATE: Clean, simple, no confusing logs.
        standby_html = """
        <div class="info-box">
            <strong style="color: #D32F2F;">System Status:</strong> 
            <br> Submit an inquiry directive to view archive retrieval logs and source evidence.
        </div>
        """
        st.markdown(standby_html, unsafe_allow_html=True)
