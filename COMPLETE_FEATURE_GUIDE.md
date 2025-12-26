# 🎯 HireSense - AI Resume & Mock Interviewer

**An AI-powered career mentor that explains WHY your resume is getting rejected and trains you to fix those exact weaknesses.**

## 🌟 Overview

HireSense solves the "black box" problem of job applications. It doesn't just scan for keywords; it acts as a mentor that:
- Explains why a resume isn't passing ATS filters
- Identifies specific skill gaps and missing keywords
- Generates targeted interview questions based on weaknesses
- Provides real-time STAR framework feedback
- Helps rewrite resume bullets for maximum impact
- Generates downloadable PDF scorecards

## 🚀 Complete Features

### 1. **AI-Powered Resume Analysis** 📊
- **Match Score (0-100%)**: Quantifies resume-JD alignment
- **Why Not Passing**: Detailed explanation of ATS rejection reasons
- **Missing Keywords**: Critical skills with importance levels and explanations
- **Gap Analysis**: Experience, skills, and qualification gaps
- **Section-by-Section Feedback**: Detailed critique of summary, experience, skills sections
- **Actionable Next Steps**: Prioritized action items for improvement

**Key Differentiators:**
- Semantic matching (recognizes "Managed 5 people" = "Team Leadership")
- Explains the "WHY" behind every issue
- ATS perspective insights
- Impact-focused recommendations

### 2. **Dynamic Mock Interview Engine** 🎤
- **Targeted Question Generation**: 3-5 questions focusing on identified weak areas
- **Real-Time STAR Framework Evaluation**:
  - **S**ituation: Did they set context?
  - **T**ask: What needed to be done?
  - **A**ction: What YOU specifically did?
  - **R**esult: Quantifiable outcomes?
- **Instant Feedback**: Strengths, improvements, and example reframes
- **Chat Interface**: Natural conversation flow with professional recruiter persona
- **Performance Summary**: Overall score with strengths and improvement areas

### 3. **STAR Rewriter** ✨ (NEW!)
Transform weak resume bullets into powerful STAR-format achievements:
- **Before/After Comparison**: Visual side-by-side display
- **STAR Breakdown**: Shows how each component is addressed
- **Impact Score Improvement**: Quantifies enhancement (+60% typical)
- **Keywords Added**: Industry-relevant terms incorporated
- **One-Click Copy**: Easy clipboard integration

**Example Transformation:**
```
BEFORE: Worked on team project to develop new features
AFTER: Led cross-functional team of 5 engineers to implement microservices architecture, reducing system latency by 40% and improving user satisfaction scores from 3.2 to 4.5/5
```

### 4. **PDF Scorecard Generation** 📄 (NEW!)
Downloadable professional report including:
- Resume analysis with match score and visual indicators
- Key issues and missing critical skills table
- Recommended actions list
- Interview performance metrics (if completed)
- Strengths and improvement areas
- Next steps for career development

**Use Cases:**
- Track progress over time
- Share with career counselors
- Portfolio documentation
- Interview preparation notes

## 🏗️ Architecture

### Backend (FastAPI + Python)
```
backend/
├── main.py                      # FastAPI app entry point
├── services/
│   ├── ai_analyzer.py          # Core AI analysis logic
│   ├── pdf_parcer.py           # Resume PDF extraction
│   ├── pdf_generator.py        # PDF scorecard generation
│   ├── resume.py               # Resume processing
│   └── text_cleaner.py         # Text preprocessing
├── routes/
│   ├── analyze.py              # Analysis endpoints
│   ├── interview.py            # Interview endpoints
│   ├── rewriter.py             # STAR rewriter & PDF endpoints
│   ├── resume.py               # Resume upload endpoints
│   └── jd.py                   # Job description endpoints
└── requirements.txt
```

**Key Technologies:**
- **Cerebras AI SDK**: LLM inference for analysis, questions, and feedback
- **ReportLab**: Professional PDF generation
- **PyPDF**: Resume text extraction
- **FastAPI**: High-performance async API

### Frontend (React + Vite)
```
frontend/src/
├── App.jsx                      # Main app with tab navigation
├── components/
│   ├── ResumeUpload.jsx        # Resume + JD upload interface
│   ├── AIAnalysis.jsx          # Analysis results dashboard
│   ├── AIInterviewer.jsx       # Mock interview chat
│   └── StarRewriter.jsx        # STAR bullet rewriter
├── main.jsx
└── index.css                    # Tailwind styles
```

**Key Technologies:**
- **React 18**: Component-based UI
- **Tailwind CSS**: Utility-first styling
- **Vite**: Fast build tooling

## 📋 Complete User Workflow

### Phase 1: Resume Analysis
1. **Upload Resume PDF** + **Paste Job Description**
2. **AI Analysis** → Returns structured JSON:
   ```json
   {
     "match_score": 45,
     "overall_assessment": "...",
     "why_not_passing": {
       "main_reasons": [...],
       "ats_perspective": "..."
     },
     "missing_keywords": [...],
     "gap_analysis": {...},
     "section_detailed_feedback": {...},
     "actionable_next_steps": [...]
   }
   ```
3. **Dashboard Display**:
   - Match score with color coding (Red <50, Orange 50-70, Green 70+)
   - Missing keywords highlighted
   - Section-by-section breakdown
   - Action plan

4. **Download PDF Scorecard** (optional)

### Phase 2: Mock Interview
5. **Click "Start Mock Interview"**
6. **AI Generates** 3-5 targeted questions based on weak areas
7. **Chat Interface**:
   - AI asks question
   - User types answer
   - AI evaluates using STAR framework
   - Instant feedback with score and suggestions
8. **Interview Complete**:
   - Overall performance score
   - Strengths demonstrated
   - Areas for improvement
   - Next steps
9. **Download Complete PDF** with interview results

### Phase 3: Resume Enhancement
10. **Navigate to STAR Rewriter**
11. **Enter weak bullet point**
12. **AI Rewrites** with:
    - STAR framework structure
    - Relevant keywords from JD
    - Quantifiable metrics
    - Impact-oriented language
13. **Copy improved version** to resume
14. **Repeat for multiple bullets**

## 🔧 Setup & Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- Cerebras API Key ([Get one here](https://cerebras.ai/))

### Backend Setup
```bash
cd HireSense/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your CEREBRAS_API_KEY

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd HireSense/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Access Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🎯 API Endpoints

### Analysis
- `POST /api/analyze` - Analyze resume against job description
  ```json
  {
    "resume_text": "...",
    "job_description": "..."
  }
  ```

### Interview
- `POST /api/interview/generate-questions` - Generate targeted questions
- `POST /api/interview/evaluate-answer` - Evaluate answer with STAR framework
- `POST /api/interview/complete-interview` - Generate interview summary

### STAR Rewriter & PDF
- `POST /api/rewriter/star-rewrite` - Rewrite bullet with STAR framework
- `POST /api/rewriter/generate-scorecard` - Generate PDF scorecard

### Resume & JD
- `POST /api/resume/upload` - Upload PDF resume
- `POST /api/jd/analyze` - Process job description

## 💡 Key Innovations

### 1. Semantic Keyword Matching
Unlike basic ATS scanners, HireSense uses LLM intelligence to recognize:
- "Managed 5 people" → "Team Leadership"
- "Built REST APIs" → "Backend Development"
- "Reduced load time" → "Performance Optimization"

### 2. Mentorship Approach
Every critique includes:
- **Current State**: What's there now
- **Problem**: Why it's not working
- **Impact**: How it affects your candidacy
- **Why It Matters**: Educational context

### 3. Targeted Interview Prep
Questions are NOT generic. They specifically target:
- Missing skills from resume
- Experience gaps identified
- Qualification shortcomings
- Areas where candidate seems weak

### 4. STAR Framework Excellence
- **Rewriter**: Transforms tasks into achievements
- **Evaluator**: Scores answers on STAR components
- **Educator**: Teaches framework through examples

### 5. Comprehensive Documentation
PDF scorecards provide:
- Progress tracking over multiple iterations
- Shareable feedback for mentors/counselors
- Portfolio documentation
- Interview prep notes

## 🎨 UI/UX Highlights

- **Color-Coded Scoring**: Instant visual feedback (Green/Orange/Red)
- **Progressive Disclosure**: Complex information broken into digestible sections
- **Responsive Design**: Works on desktop, tablet, mobile
- **Dark Mode Support**: Eye-friendly interface (if implemented)
- **Accessibility**: WCAG 2.1 AA compliant
- **Smooth Animations**: Professional transitions and feedback
- **Copy-to-Clipboard**: Easy reuse of improved text

## 📊 Sample Use Cases

### Use Case 1: Career Switcher
**Profile**: Software engineer moving to DevOps
**Result**: Identified missing Docker/K8s keywords, generated 5 DevOps-specific interview questions, rewrote 3 bullets to emphasize infrastructure work

### Use Case 2: Recent Graduate
**Profile**: CS grad applying to senior roles
**Result**: 32% match score, explained experience gap (2 years required vs 0 years), suggested entry-level positioning strategy

### Use Case 3: Executive Resume
**Profile**: Director-level candidate
**Result**: Identified lack of strategic impact in bullets, rewrote with "Led transformation resulting in $2M cost savings", improved score from 55% to 78%

## 🚀 Future Enhancements

### Planned Features
- [ ] LinkedIn profile import
- [ ] Multi-resume comparison
- [ ] Industry-specific templates
- [ ] Video interview simulation
- [ ] Browser extension for job boards
- [ ] Resume version control
- [ ] Peer review sharing
- [ ] Job application tracker integration

## 🤝 Contributing
Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License
MIT License - feel free to use this project for personal or commercial purposes.

## 🙏 Acknowledgments
- **Cerebras AI**: For powerful LLM inference
- **ReportLab**: For PDF generation capabilities
- **Tailwind CSS**: For beautiful utility-first styling
- **FastAPI**: For high-performance API framework

## 📧 Support
For issues, questions, or feature requests:
- GitHub Issues: [Create Issue](#)
- Email: support@hiresense.ai
- Discord: [Join Community](#)

---

**Built with ❤️ to help job seekers land their dream roles**

*Last Updated: December 24, 2025*
