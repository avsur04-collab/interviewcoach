# AI Interview Coach Pro - Dual-AI System

🎯 **The Best of Both Worlds**: Gemini's superior video analysis + Claude's strategic coaching

## 🧠 How the Dual-AI System Works

### Step 1: Question Generation
**Claude Sonnet 4** analyzes your resume and job description to create a personalized, high-stakes interview question.

### Step 2: Video Analysis  
**Gemini 2.0 Flash** watches your video and observes:
- Body language, posture, gestures
- Eye contact and facial expressions
- Tone, pace, and vocal confidence
- Content structure and time management

### Step 3: Coaching Feedback
**Claude Sonnet 4** takes Gemini's observations and provides:
- Strategic coaching on what you nailed
- Actionable improvements with examples
- Pro tips to elevate your next answer

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install streamlit google-generativeai anthropic
```

### 2. Run Locally
```bash
streamlit run interview_coach_hybrid.py
```

### 3. Get API Keys

**Google Gemini API Key** (FREE tier available):
- Go to: https://makersuite.google.com/app/apikey
- Click "Create API Key"
- Copy your key

**Anthropic Claude API Key** (FREE $5 credit):
- Go to: https://console.anthropic.com/
- Sign up for an account
- Get your API key from Settings

## 🌐 Deploy as Public URL

### Option 1: Streamlit Community Cloud (100% FREE)

1. **Create GitHub Repository**
   - Go to https://github.com
   - New repository: `interview-coach-pro`
   - Upload these files:
     - `interview_coach_hybrid.py`
     - `requirements.txt`

2. **Deploy on Streamlit**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Connect your GitHub repo
   - Main file: `interview_coach_hybrid.py`
   - Click "Deploy"

3. **Configure Secrets (Optional)**
   - In Streamlit Cloud: App Settings → Secrets
   - Add shared API keys (or let users enter their own)

```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "your-gemini-key-here"
CLAUDE_API_KEY = "your-claude-key-here"
```

4. **Share Your URL**
   - Get: `yourname-interview-coach-pro.streamlit.app`
   - Send to anyone!

### Option 2: Hugging Face Spaces
1. Go to https://huggingface.co/spaces
2. Create Space with Streamlit SDK
3. Upload files
4. Add secrets in Settings

## 💰 Cost Breakdown

### Free Tier Limits:

**Gemini 2.0 Flash**:
- 15 requests per minute
- 1,500 requests per day
- 1 million requests per month
- **More than enough for personal use!**

**Claude Sonnet 4**:
- $5 free credit (lasts ~125 video analyses)
- After that: ~$0.04 per video analysis
- **Very affordable even at scale**

### What This Means:
- **Personal use**: Completely FREE
- **Sharing with friends**: Still FREE
- **100+ users/day**: ~$4/day in Claude costs

## 🎯 Why This Architecture is Superior

| Feature | Gemini Only | Claude Only | **Dual-AI (This!)** |
|---------|-------------|-------------|---------------------|
| Video Analysis | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Body Language | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Strategic Coaching | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Reasoning Depth | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Question Quality | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 📱 Features

✅ **Personalized Questions**: Claude analyzes job + resume  
✅ **Multimodal Video Analysis**: Gemini sees everything  
✅ **Strategic Coaching**: Claude provides deep insights  
✅ **Download Reports**: Save complete feedback  
✅ **Side-by-side Comparison**: See both AI's outputs  
✅ **Mobile Friendly**: Works everywhere  

## 🛠️ Advanced: Modify the Prompts

Both AI systems use carefully crafted prompts. You can customize them in the code:

**Gemini's observation prompt** (line ~270):
- Controls what Gemini looks for in videos
- Add industry-specific body language cues

**Claude's coaching prompt** (line ~310):
- Controls the feedback structure
- Add role-specific coaching frameworks

## 🔒 Privacy & Security

- Videos are processed temporarily and deleted immediately
- API keys are stored in your browser session only
- No data is stored permanently
- Use Streamlit secrets for shared deployments

## 💡 Pro Tips

### For Recording:
- Good lighting (face the window)
- Eye-level camera (stack books)
- Plain background
- Test audio first
- Practice 2-3 takes

### For Best Feedback:
- Record multiple attempts
- Compare feedback across tries
- Focus on one improvement at a time
- Download reports to track progress

## 📊 Example Workflow

1. **Morning**: Generate 3 questions for different roles
2. **Afternoon**: Record responses to all 3
3. **Evening**: Review all feedback, identify patterns
4. **Next Day**: Re-record with improvements
5. **Compare**: See measurable progress!

## 🆘 Troubleshooting

**"API Key Error"**
- Check keys are entered correctly
- Ensure you have credits remaining
- Try regenerating the API key

**"Video Processing Failed"**
- Ensure video is MP4 format
- Keep under 60 seconds
- File size under 100MB
- Good internet connection

**"Slow Analysis"**
- Gemini processes videos (10-30 seconds normal)
- Larger videos = longer processing
- Be patient during "Processing..." stage

## 🎓 Learning Resources

**Improve Your Interviews**:
- STAR Method framework
- Behavioral interview prep
- Technical interview guides

**API Documentation**:
- Gemini: https://ai.google.dev/docs
- Claude: https://docs.anthropic.com

## 📄 License

Free to use, modify, and distribute. Build amazing things!

---

**Built with ❤️ using:**
- Streamlit for the interface
- Google Gemini 2.0 Flash for video analysis
- Anthropic Claude Sonnet 4 for strategic coaching
