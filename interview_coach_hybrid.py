import streamlit as st
import google.generativeai as genai
import anthropic
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="AI Interview Coach Pro",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom right, #EFF6FF, #E0E7FF);
    }
    .stButton>button {
        width: 100%;
        background-color: #4F46E5;
        color: white;
        font-weight: 600;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        transform: translateY(-2px);
    }
    .question-box {
        background-color: #EEF2FF;
        border: 2px solid #C7D2FE;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .feedback-box {
        background-color: #F9FAFB;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .ai-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    .gemini-badge {
        background-color: #DBEAFE;
        color: #1E40AF;
    }
    .claude-badge {
        background-color: #FEE2E2;
        color: #991B1B;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'interview_question' not in st.session_state:
    st.session_state.interview_question = ""
if 'gemini_observations' not in st.session_state:
    st.session_state.gemini_observations = ""
if 'claude_feedback' not in st.session_state:
    st.session_state.claude_feedback = ""

# API Keys in sidebar
with st.sidebar:
    st.title("⚙️ API Configuration")
    
    st.markdown("### 🔵 Google Gemini")
    gemini_key = st.text_input("Gemini API Key", type="password", help="For video analysis")
    if gemini_key:
        genai.configure(api_key=gemini_key)
        st.success("✅ Gemini configured!")
    else:
        st.warning("⚠️ Enter Gemini key")
    
    st.markdown("### 🔴 Anthropic Claude")
    claude_key = st.text_input("Claude API Key", type="password", help="For coaching feedback")
    if claude_key:
        st.success("✅ Claude configured!")
    else:
        st.warning("⚠️ Enter Claude key")
    
    st.divider()
    
    st.markdown("### 🎯 How It Works")
    st.markdown("""
    <div style="font-size: 0.85rem; line-height: 1.6;">
    <span class="ai-badge gemini-badge">GEMINI</span> analyzes your video for:
    • Body language & gestures
    • Tone & speaking pace
    • Visual confidence
    • Audio-visual sync
    
    <span class="ai-badge claude-badge">CLAUDE</span> provides coaching on:
    • Content structure
    • Answer quality
    • Strategic improvements
    • Actionable next steps
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 📊 Progress")
    st.markdown(f"**Current Step:** {st.session_state.step}/3")
    
    if st.session_state.step > 1:
        if st.button("🔄 Start Over"):
            st.session_state.step = 1
            st.session_state.job_description = ""
            st.session_state.resume_text = ""
            st.session_state.interview_question = ""
            st.session_state.gemini_observations = ""
            st.session_state.claude_feedback = ""
            st.rerun()

# Header
st.title("🎯 AI Interview Coach Pro")
st.markdown("**Powered by Gemini's Video Analysis + Claude's Reasoning**")
st.divider()

# Progress indicator
col1, col2, col3 = st.columns(3)
with col1:
    if st.session_state.step >= 1:
        st.markdown("✅ **1. Setup**")
    else:
        st.markdown("⚪ 1. Setup")
with col2:
    if st.session_state.step >= 2:
        st.markdown("✅ **2. Record**")
    else:
        st.markdown("⚪ 2. Record")
with col3:
    if st.session_state.step >= 3:
        st.markdown("✅ **3. Feedback**")
    else:
        st.markdown("⚪ 3. Feedback")

st.divider()

# STEP 1: Upload Materials
if st.session_state.step == 1:
    st.header("📄 Step 1: Upload Your Materials")
    
    if not claude_key:
        st.error("⚠️ Please enter your Claude API key in the sidebar to generate questions")
        st.stop()
    
    # Job Description
    st.subheader("Job Description")
    job_description = st.text_area(
        "Paste the full job description here",
        value=st.session_state.job_description,
        height=200,
        placeholder="Enter the complete job posting..."
    )
