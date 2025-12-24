# HireSense - AI Resume Mentor 🎯

## Stage 1 Feature: "Why Your Resume Isn't Passing" Analysis

### Overview
HireSense acts as your personal **career mentor**, not just a resume scanner. It explains **WHY** your resume fails ATS screening and provides detailed, actionable insights to help you understand and fix the gaps.

### What Makes This Different?
Unlike traditional ATS scanners that just show keyword matches, HireSense:
- **Explains the "Why"**: Detailed reasoning behind each issue
- **Acts as a Mentor**: Educational feedback that teaches you about ATS systems
- **Identifies Root Causes**: Goes beyond missing keywords to explain fundamental gaps
- **Provides Context**: Each issue includes its impact on your candidacy
- **Actionable Steps**: Prioritized action plan to improve your resume

---

## Features Implemented ✅

### 1. **Comprehensive Match Score**
- 0-100% ATS compatibility score
- Overall assessment explaining if resume would pass initial screening
- Clear pass/fail threshold context

### 2. **Why Not Passing Analysis**
Detailed breakdown including:
- **Main Reasons**: 3-5 fundamental issues preventing passage
- **ATS Perspective**: How automated systems view your resume
- Explanation of keyword matching and semantic relevance

### 3. **Critical Missing Keywords**
For each missing keyword:
- **Keyword**: The specific term missing
- **Importance Level**: Critical / High / Medium
- **Why It Matters**: Detailed explanation of impact on your candidacy
- Context about role requirements and technical expectations

### 4. **Gap Analysis**
Three-dimensional gap assessment:

#### Experience Gaps
- What the job requires vs. what resume shows
- Specific experience mismatches
- How to position existing experience better

#### Skills Gaps
- Technical skill deficiencies
- Day-1 requirements you're missing
- Tool and technology gaps

#### Qualification Gaps
- Education and certification needs
- Professional credentials that could help
- Validation opportunities

### 5. **Section-by-Section Feedback**
For Summary, Experience, and Skills sections:
- **Current State**: What's currently present (or missing)
- **Problem**: Why it's not working for this specific role
- **Impact**: How this affects ATS scoring and human review

### 6. **Actionable Next Steps**
Prioritized action plan:
- Ordered by importance (most critical first)
- Specific, implementable actions
- Quick wins vs. longer-term improvements
- Practical guidance for resume revision

---

## How It Works

### Backend Architecture
```
User uploads PDF → Extract text → Cerebras AI Analysis → Mentor-style feedback
```

**Tech Stack:**
- **AI Model**: Cerebras Llama-3.3-70b (fast inference)
- **Backend**: FastAPI with Python
- **PDF Processing**: PyPDF for text extraction
- **Prompt Engineering**: Mentor-focused system prompts

### Frontend Experience
```
Single-page app → Upload PDF + JD → Comprehensive visual analysis
```

**Tech Stack:**
- **Framework**: React with Vite
- **Styling**: Tailwind CSS
- **Components**: Color-coded feedback sections

---

## Usage

### 1. Start Backend Server
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or use the convenience script:
```bash
cd backend
./run_server.sh
```

### 2. Start Frontend
```bash
cd frontend
npm run dev
```

### 3. Upload & Analyze
1. Upload your resume PDF
2. Paste the job description
3. Click "Process Resume"
4. Review comprehensive mentor-style feedback

---

## API Endpoints

### `POST /api/resume/upload`
Upload PDF and extract text
```json
{
  "filename": "resume.pdf",
  "resume_text": "extracted text..."
}
```

### `POST /api/analyze`
Analyze resume against job description
```json
{
  "resume_text": "...",
  "job_description": "..."
}
```

**Response Structure:**
```json
{
  "match_score": 45,
  "overall_assessment": "...",
  "why_not_passing": {
    "main_reasons": [...],
    "ats_perspective": "..."
  },
  "missing_keywords": [
    {
      "keyword": "Docker",
      "importance": "critical",
      "why_matters": "..."
    }
  ],
  "gap_analysis": {
    "experience_gaps": "...",
    "skills_gaps": "...",
    "qualification_gaps": "..."
  },
  "section_detailed_feedback": {
    "summary": {
      "current_state": "...",
      "problem": "...",
      "impact": "..."
    },
    ...
  },
  "actionable_next_steps": [...]
}
```

---

## Configuration

### Environment Variables (backend/.env)
```bash
# Cerebras AI API Key
CEREBRAS_API_KEY=your-api-key-here

# Model Selection
CEREBRAS_MODEL=llama-3.3-70b
```

### Get Your Cerebras API Key
1. Visit https://cerebras.ai/
2. Sign up for developer access
3. Generate API key
4. Add to `.env` file

---

## Key Design Decisions

### Why Cerebras AI?
- **Fast Inference**: Sub-second response times
- **Cost-Effective**: Better pricing than GPT-4
- **Llama 3.3 70B**: Strong reasoning capabilities
- **Reliable JSON**: Consistent structured output

### Why Mentor Approach?
- **Educational**: Users learn about ATS systems
- **Empowering**: Understand gaps, don't just fix blindly
- **Contextual**: "Why" matters more than "what"
- **Actionable**: Knowledge leads to better improvements

### Why Detailed Feedback?
- **Transparency**: No black box scoring
- **Specificity**: Concrete issues to address
- **Prioritization**: Focus on what matters most
- **Confidence**: Know exactly what to improve

---

## Future Enhancements (Stage 2+)

### Planned Features:
- [ ] **Mock Interview Generator**: Practice questions based on identified gaps
- [ ] **Resume Rewriter**: AI-assisted resume improvements
- [ ] **Skills Gap Practice**: Technical question banks for missing skills
- [ ] **Progress Tracking**: Save analyses and track improvements
- [ ] **Industry Templates**: Role-specific resume guidance
- [ ] **ATS Optimization Score**: Real-time editing feedback

---

## Project Structure

```
HireSense/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── .env                    # Environment variables (Cerebras key)
│   ├── requirements.txt        # Python dependencies
│   ├── routes/
│   │   ├── analyze.py         # Analysis endpoint
│   │   └── resume.py          # PDF upload endpoint
│   └── services/
│       ├── ai_analyzer.py     # Cerebras AI integration (MENTOR LOGIC)
│       ├── pdf_parser.py      # PDF text extraction
│       └── text_cleaner.py    # Text preprocessing
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main application (ANALYSIS UI)
│   │   └── components/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## Contributing

### Key Areas to Enhance:
1. **Prompt Engineering**: Improve mentor feedback quality
2. **UI/UX**: Better visualization of gaps and feedback
3. **Analysis Depth**: Add more sections (Projects, Education, etc.)
4. **Export Options**: PDF reports, email summaries
5. **Comparison Mode**: Compare multiple resume versions

---

## License
MIT

---

## Support

For issues or questions:
1. Check backend logs for API errors
2. Verify Cerebras API key is valid
3. Ensure frontend can reach backend (CORS)
4. Review sample analysis output in mock response

---

**Built with ❤️ to help job seekers understand and improve their applications**
