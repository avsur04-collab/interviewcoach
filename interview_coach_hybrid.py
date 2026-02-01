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
    st.session_state.job_description = job_description
    
    st.divider()
    
    # Resume Input
    st.subheader("Resume/Portfolio")
    
    tab1, tab2 = st.tabs(["📄 Upload PDF", "✍️ Paste Text"])
    
    with tab1:
        resume_file = st.file_uploader("Upload your resume (PDF)", type=['pdf'])
        if resume_file:
            st.success(f"✅ Uploaded: {resume_file.name}")
    
    with tab2:
        resume_text = st.text_area(
            "Or paste your resume text here",
            value=st.session_state.resume_text,
            height=200,
            placeholder="Paste your resume content..."
        )
        st.session_state.resume_text = resume_text
    
    st.divider()
    
    # Generate Question Button
    if st.button("🚀 Generate Interview Question", disabled=not (job_description and (resume_file or resume_text))):
        with st.spinner("🤔 Claude is analyzing your materials and generating a high-stakes question..."):
            try:
                # Initialize Claude client
                client = anthropic.Anthropic(api_key=claude_key)
                
                # Get resume content
                if resume_file:
                    import base64
                    resume_bytes = resume_file.read()
                    resume_b64 = base64.b64encode(resume_bytes).decode('utf-8')
                    
                    # Use Claude to extract text from PDF
                    extract_message = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=1000,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "document",
                                        "source": {
                                            "type": "base64",
                                            "media_type": "application/pdf",
                                            "data": resume_b64
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": "Extract all text from this resume/portfolio document."
                                    }
                                ]
                            }
                        ]
                    )
                    resume_content = extract_message.content[0].text
                else:
                    resume_content = resume_text
                
                # Generate interview question with Claude
                question_message = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1000,
                    messages=[
                        {
                            "role": "user",
                            "content": f"""You are an expert interview coach. Analyze this job description and candidate resume to generate ONE high-stakes interview question.

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{resume_content}

Generate a challenging, role-specific interview question that:
1. Tests critical skills mentioned in the job description
2. Connects to the candidate's background
3. Requires thoughtful analysis (not just recitation)
4. Can be answered well in 60 seconds

Return ONLY the question, no preamble or explanation."""
                        }
                    ]
                )
                
                st.session_state.interview_question = question_message.content[0].text
                st.session_state.step = 2
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error generating question: {str(e)}")

# STEP 2: Record Video Response
elif st.session_state.step == 2:
    st.header("🎥 Step 2: Record Your Response")
    
    # Display the question
    st.markdown(f"""
    <div class="question-box">
        <h3 style="color: #4338CA; margin-bottom: 1rem;">
            📌 Your Interview Question 
            <span class="ai-badge claude-badge">Generated by Claude</span>
        </h3>
        <p style="font-size: 1.1rem; line-height: 1.6; color: #1F2937;">{st.session_state.interview_question}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Video upload
    st.subheader("Upload Your Video Response")
    st.info("📹 Record a 60-second (or less) video answering the question above. Save as MP4 format.")
    
    video_file = st.file_uploader("Upload your video response (MP4)", type=['mp4'])
    
    if video_file:
        st.success(f"✅ Uploaded: {video_file.name}")
        
        # Preview video
        st.subheader("Preview Your Response")
        st.video(video_file)
    
    st.divider()
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Back to Setup"):
            st.session_state.step = 1
            st.rerun()
    
    with col2:
        if st.button("🎯 Get AI Feedback", disabled=not video_file or not (gemini_key and claude_key)):
            with st.spinner("🔍 Step 1/2: Gemini is analyzing your video..."):
                try:
                    # Save video temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                        tmp_file.write(video_file.read())
                        tmp_path = tmp_file.name
                    
                    # Upload video to Gemini
                    uploaded_video = genai.upload_file(tmp_path)
                    
                    # Wait for processing
                    import time
                    while uploaded_video.state.name == "PROCESSING":
                        time.sleep(2)
                        uploaded_video = genai.get_file(uploaded_video.name)
                    
                    if uploaded_video.state.name == "FAILED":
                        raise Exception("Video processing failed")
                    
                    # Configure Gemini for video analysis
                    gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
                    
                    # Get Gemini's multimodal observations
                    gemini_prompt = f"""Analyze this interview response video and provide ONLY observations about the candidate's delivery and presence. Do NOT provide coaching advice.

INTERVIEW QUESTION ASKED:
{st.session_state.interview_question}

Observe and report on:

1. **VISUAL PRESENCE**
   - Body language and posture
   - Eye contact and gaze
   - Facial expressions
   - Hand gestures and movement
   - Overall confidence level

2. **VOCAL DELIVERY**
   - Speaking pace (too fast/slow/just right)
   - Tone and energy
   - Clarity and articulation
   - Vocal confidence
   - Filler words or pauses

3. **CONTENT DELIVERY**
   - How they structured their answer
   - Time management (did they finish in 60 seconds?)
   - Key points they covered
   - Examples or stories used

Be specific and objective. Report what you observe without judgment. These observations will be sent to another AI coach for interpretation."""

                    gemini_response = gemini_model.generate_content([uploaded_video, gemini_prompt])
                    st.session_state.gemini_observations = gemini_response.text
                    
                    # Clean up video file
                    os.unlink(tmp_path)
                    
                except Exception as e:
                    st.error(f"❌ Error with Gemini analysis: {str(e)}")
                    st.stop()
            
            # Now use Claude for coaching
            with st.spinner("💡 Step 2/2: Claude is generating your personalized coaching report..."):
                try:
                    client = anthropic.Anthropic(api_key=claude_key)
                    
                    claude_prompt = f"""You are an expert interview coach. You've received detailed observations from a video analysis AI about a candidate's interview response.

INTERVIEW QUESTION:
{st.session_state.interview_question}

JOB CONTEXT:
{st.session_state.job_description}

VIDEO ANALYSIS OBSERVATIONS (from Gemini AI):
{st.session_state.gemini_observations}

Based on these observations, provide a 'REDIRECTION REPORT' with strategic coaching advice:

## ✅ What You Nailed
Identify 2-3 specific strengths from the observations. Be concrete and encouraging.

## 🎯 What Needs Improvement  
Identify 2-3 specific areas for improvement with actionable advice. Explain WHY these matter and HOW to fix them.

## 💡 Pro Tip for Next Time
Provide ONE powerful technique or framework that would elevate this type of answer significantly.

Be direct, constructive, and specific. Your goal is to help this person improve and land the job."""

                    claude_response = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=2000,
                        messages=[
                            {
                                "role": "user",
                                "content": claude_prompt
                            }
                        ]
                    )
                    
                    st.session_state.claude_feedback = claude_response.content[0].text
                    st.session_state.step = 3
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error with Claude coaching: {str(e)}")

# STEP 3: View Feedback
elif st.session_state.step == 3:
    st.header("🎉 Your Dual-AI Redirection Report")
    
    # Display the question asked
    st.markdown(f"""
    <div class="question-box">
        <h3 style="color: #4338CA; margin-bottom: 1rem;">📌 Question Asked:</h3>
        <p style="font-size: 1rem; color: #1F2937;">{st.session_state.interview_question}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Tabs for different feedback
    tab1, tab2 = st.tabs([
        "🎯 Claude's Coaching Report",
        "🔍 Gemini's Raw Observations"
    ])
    
    with tab1:
        st.markdown(f"""
        <div style="background-color: #FEF2F2; border-left: 4px solid #991B1B; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <strong>Powered by Claude Sonnet 4</strong> - Strategic reasoning and coaching expertise
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(st.session_state.claude_feedback)
    
    with tab2:
        st.markdown(f"""
        <div style="background-color: #EFF6FF; border-left: 4px solid #1E40AF; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <strong>Powered by Gemini 2.0 Flash</strong> - Multimodal video analysis
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(st.session_state.gemini_observations)
    
    st.divider()
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Practice Another Question"):
            st.session_state.step = 1
            st.session_state.interview_question = ""
            st.session_state.gemini_observations = ""
            st.session_state.claude_feedback = ""
            st.rerun()
    
    with col2:
        # Download complete report
        full_report = f"""AI INTERVIEW COACH - COMPLETE REPORT
{'='*60}

QUESTION ASKED:
{st.session_state.interview_question}

{'='*60}
CLAUDE'S COACHING REPORT (Strategic Feedback)
{'='*60}

{st.session_state.claude_feedback}

{'='*60}
GEMINI'S VIDEO OBSERVATIONS (Multimodal Analysis)
{'='*60}

{st.session_state.gemini_observations}

{'='*60}
Powered by Gemini 2.0 Flash + Claude Sonnet 4
"""
        
        st.download_button(
            label="💾 Download Complete Report",
            data=full_report,
            file_name="interview_feedback_complete.txt",
            mime="text/plain"
        )

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #6B7280; padding: 2rem 0;">
        <p><strong>Dual-AI Architecture:</strong> Gemini 2.0 Flash (Video Analysis) + Claude Sonnet 4 (Strategic Coaching)</p>
        <p style="font-size: 0.85rem; margin-top: 0.5rem;">Get your API keys: 
        <a href="https://makersuite.google.com/app/apikey" target="_blank">Gemini</a> • 
        <a href="https://console.anthropic.com/" target="_blank">Claude</a>
        </p>
    </div>
""", unsafe_allow_html=True)
