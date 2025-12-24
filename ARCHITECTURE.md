# 🎯 HireSense - System Architecture & Data Flow

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        USER BROWSER                          │
│                    http://localhost:5173                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ HTTP/REST API
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    FRONTEND (React + Vite)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Resume      │  │    Mock      │  │    STAR      │     │
│  │  Analysis    │  │  Interview   │  │  Rewriter    │     │
│  │  Dashboard   │  │    Chat      │  │  Transform   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                  │              │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │
                             │ Fetch API
                             │
┌────────────────────────────▼─────────────────────────────────┐
│                  BACKEND (FastAPI Python)                     │
│                  http://localhost:8000                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   API ROUTES                          │   │
│  │  /api/analyze          │  /api/interview/*           │   │
│  │  /api/rewriter/*       │  /api/resume/upload         │   │
│  └──────────────┬─────────┴─────────────────────────────┘   │
│                 │                                             │
│  ┌──────────────▼──────────────────────────────────────┐   │
│  │                    SERVICES                          │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐   │   │
│  │  │AI Analyzer │  │PDF Parcer  │  │PDF Generator│   │   │
│  │  │            │  │            │  │            │   │   │
│  │  │• Analysis  │  │• Extract   │  │• Scorecard │   │   │
│  │  │• Questions │  │  Text      │  │• ReportLab │   │   │
│  │  │• Evaluate  │  │• PyPDF     │  │• Formatting│   │   │
│  │  │• Rewrite   │  └────────────┘  └────────────┘   │   │
│  │  └──────┬─────┘                                     │   │
│  └─────────┼────────────────────────────────────────────┘   │
└────────────┼──────────────────────────────────────────────────┘
             │
             │ API Call
             │
┌────────────▼──────────────────────────────────────────────────┐
│                     CEREBRAS AI API                            │
│                    (LLM Inference)                             │
│                  Model: llama-3.3-70b                         │
└───────────────────────────────────────────────────────────────┘
```

---

## 📊 Complete Data Flow Diagram

### Flow 1: Resume Analysis
```
USER                    FRONTEND              BACKEND                 AI
 │                         │                     │                    │
 │ 1. Upload PDF           │                     │                    │
 │ + Job Description       │                     │                    │
 ├──────────────────────>  │                     │                    │
 │                         │ 2. POST /api/       │                    │
 │                         │    interview/       │                    │
 │                         │    start-interview  │                    │
 │                         ├──────────────────>  │                    │
 │                         │                     │ 3. Extract PDF     │
 │                         │                     │    text            │
 │                         │                     │                    │
 │                         │                     │ 4. Build analysis  │
 │                         │                     │    prompts         │
 │                         │                     ├─────────────────>  │
 │                         │                     │                    │
 │                         │                     │  5. AI Analysis    │
 │                         │                     │     Processing     │
 │                         │                     │  ⏱️ 5-15 seconds   │
 │                         │                     │                    │
 │                         │                     │  <-----------------│
 │                         │  6. Analysis JSON   │                    │
 │                         │  {                  │                    │
 │                         │    match_score,     │                    │
 │                         │    missing_keywords,│                    │
 │                         │    gap_analysis,    │                    │
 │                         │    feedback...      │                    │
 │                         │  }                  │                    │
 │  7. Display Analysis    │  <-----------------│                    │
 │  Dashboard              │                     │                    │
 │  <──────────────────────│                     │                    │
 │                         │                     │                    │
 │ 8. Click "Download      │                     │                    │
 │    PDF Scorecard"       │                     │                    │
 │ ───────────────────────>│ 9. POST /api/       │                    │
 │                         │    rewriter/        │                    │
 │                         │    generate-        │                    │
 │                         │    scorecard        │                    │
 │                         ├──────────────────>  │                    │
 │                         │                     │ 10. Generate PDF   │
 │                         │                     │     with ReportLab │
 │                         │  11. PDF Bytes      │                    │
 │  12. Download PDF       │  <─────────────────│                    │
 │  <──────────────────────│                     │                    │
```

### Flow 2: Mock Interview
```
USER                    FRONTEND              BACKEND                 AI
 │                         │                     │                    │
 │ 1. Click "Start         │                     │                    │
 │    Mock Interview"      │                     │                    │
 ├──────────────────────>  │                     │                    │
 │                         │ 2. POST /api/       │                    │
 │                         │    interview/       │                    │
 │                         │    generate-        │                    │
 │                         │    questions        │                    │
 │                         ├──────────────────>  │                    │
 │                         │                     │ 3. Build question  │
 │                         │                     │    generation      │
 │                         │                     │    prompt with     │
 │                         │                     │    missing skills  │
 │                         │                     ├─────────────────>  │
 │                         │                     │  4. Generate 5     │
 │                         │                     │     targeted Qs    │
 │                         │                     │  ⏱️ 3-8 seconds    │
 │                         │                     │  <─────────────────│
 │                         │  5. Questions Array │                    │
 │  6. Display Q1          │  <─────────────────│                    │
 │  <──────────────────────│                     │                    │
 │                         │                     │                    │
 │ 7. Type Answer          │                     │                    │
 │    and Submit           │                     │                    │
 │ ───────────────────────>│ 8. POST /api/       │                    │
 │                         │    interview/       │                    │
 │                         │    evaluate-answer  │                    │
 │                         ├──────────────────>  │                    │
 │                         │                     │ 9. Build STAR      │
 │                         │                     │    evaluation      │
 │                         │                     │    prompt          │
 │                         │                     ├─────────────────>  │
 │                         │                     │  10. Evaluate      │
 │                         │                     │      using STAR    │
 │                         │                     │  ⏱️ 2-5 seconds    │
 │                         │                     │  <─────────────────│
 │                         │  11. Feedback JSON  │                    │
 │                         │  {                  │                    │
 │                         │    score: 75,       │                    │
 │                         │    star_analysis,   │                    │
 │                         │    strengths,       │                    │
 │                         │    improvements     │                    │
 │                         │  }                  │                    │
 │  12. Show Feedback      │  <─────────────────│                    │
 │  <──────────────────────│                     │                    │
 │                         │                     │                    │
 │  [Repeat Q2-Q5...]      │                     │                    │
 │                         │                     │                    │
 │ 13. Complete Interview  │ 14. POST /api/      │                    │
 │ ───────────────────────>│     interview/      │                    │
 │                         │     complete        │                    │
 │                         ├──────────────────>  │                    │
 │                         │                     │ 15. Generate       │
 │                         │                     │     summary        │
 │                         │  16. Summary JSON   │                    │
 │  17. Display Results    │  <─────────────────│                    │
 │  <──────────────────────│                     │                    │
```

### Flow 3: STAR Rewriter
```
USER                    FRONTEND              BACKEND                 AI
 │                         │                     │                    │
 │ 1. Navigate to          │                     │                    │
 │    STAR Rewriter        │                     │                    │
 │    Tab                  │                     │                    │
 ├──────────────────────>  │                     │                    │
 │                         │                     │                    │
 │ 2. Enter weak bullet:   │                     │                    │
 │    "Worked on project"  │                     │                    │
 │                         │                     │                    │
 │ 3. Click "Rewrite"      │                     │                    │
 ├──────────────────────>  │ 4. POST /api/       │                    │
 │                         │    rewriter/        │                    │
 │                         │    star-rewrite     │                    │
 │                         ├──────────────────>  │                    │
 │                         │                     │ 5. Build STAR      │
 │                         │                     │    rewrite prompt  │
 │                         │                     │    with JD context │
 │                         │                     ├─────────────────>  │
 │                         │                     │  6. Transform      │
 │                         │                     │     bullet with    │
 │                         │                     │     STAR + metrics │
 │                         │                     │  ⏱️ 3-7 seconds    │
 │                         │                     │  <─────────────────│
 │                         │  7. Rewrite Result  │                    │
 │                         │  {                  │                    │
 │                         │    original,        │                    │
 │                         │    rewritten:       │                    │
 │                         │    "Led team of 5   │                    │
 │                         │     engineers...",  │                    │
 │                         │    star_breakdown,  │                    │
 │                         │    keywords_added,  │                    │
 │                         │    impact_score+60% │                    │
 │                         │  }                  │                    │
 │  8. Display Before/     │  <─────────────────│                    │
 │     After Comparison    │                     │                    │
 │  <──────────────────────│                     │                    │
 │                         │                     │                    │
 │ 9. Click Copy           │                     │                    │
 │ ───────────────────────>│ 10. Copy to         │                    │
 │                         │     Clipboard       │                    │
 │  11. Paste in Resume    │                     │                    │
 │  <──────────────────────│                     │                    │
```

---

## 🗄️ Data Models

### Analysis Response Model
```typescript
interface AnalysisResponse {
  match_score: number;                    // 0-100
  overall_assessment: string;
  why_not_passing: {
    main_reasons: string[];               // 3-5 reasons
    ats_perspective: string;
  };
  missing_keywords: Array<{
    keyword: string;
    importance: 'critical' | 'high' | 'medium';
    why_matters: string;
  }>;
  gap_analysis: {
    experience_gaps: string;
    skills_gaps: string;
    qualification_gaps: string;
  };
  section_detailed_feedback: {
    [section: string]: {
      current_state: string;
      problem: string;
      impact: string;
    };
  };
  actionable_next_steps: string[];        // 5-7 steps
}
```

### Interview Question Model
```typescript
interface InterviewQuestion {
  question: string;
  category: 'technical' | 'behavioral' | 'situational';
  focus_area: string;                     // Which weakness
  why_asking: string;
}
```

### STAR Evaluation Model
```typescript
interface STAREvaluation {
  score: number;                          // 0-100
  star_analysis: {
    situation: 'present' | 'missing' | 'weak';
    task: 'present' | 'missing' | 'weak';
    action: 'present' | 'missing' | 'weak';
    result: 'present' | 'missing' | 'weak';
  };
  strengths: string[];                    // 2-3 points
  improvements: string[];                 // 2-3 points
  suggestion: string;
  example_reframe: string;
}
```

### STAR Rewrite Model
```typescript
interface STARRewrite {
  original: string;
  rewritten: string;
  improvements: {
    before_issues: string[];
    after_strengths: string[];
  };
  star_breakdown: {
    situation: string;
    task: string;
    action: string;
    result: string;
  };
  keywords_added: string[];
  impact_score_improvement: number;       // 0-100
}
```

---

## 🔄 State Management Flow

### Frontend State (React)
```javascript
App.jsx State:
├── analysisData: object | null          // From backend
├── activeTab: 'upload' | 'interview' | 'rewriter'
└── interviewSummary: object | null

ResumeUpload.jsx State:
├── resumeFile: File | null
├── jobDescription: string
├── loading: boolean
└── error: string

AIAnalysis.jsx State:
└── downloadingPDF: boolean

AIInterviewer.jsx State:
├── messages: Array<Message>
├── currentQuestion: string
├── currentQuestionIndex: number
├── userAnswer: string
├── loading: boolean
├── interviewStarted: boolean
├── interviewComplete: boolean
├── questions: Array<Question>
├── answers: Array<Answer>
└── feedback: object | null

StarRewriter.jsx State:
├── originalBullet: string
├── rewriteResult: object | null
├── loading: boolean
└── error: string
```

---

## 🎯 API Endpoint Reference

### Analysis
```
POST /api/analyze
Body: { resume_text, job_description }
Response: AnalysisResponse
⏱️ 5-15 seconds
```

### Interview
```
POST /api/interview/generate-questions
Body: { resume_text, job_description, analysis, question_count }
Response: { questions: Question[] }
⏱️ 3-8 seconds

POST /api/interview/evaluate-answer
Body: { question, answer, job_description }
Response: STAREvaluation
⏱️ 2-5 seconds

POST /api/interview/complete-interview
Body: { questions, answers, analysis }
Response: InterviewSummary
⏱️ 1-3 seconds
```

### STAR Rewriter & PDF
```
POST /api/rewriter/star-rewrite
Body: { original_bullet, job_description, resume_context }
Response: STARRewrite
⏱️ 3-7 seconds

POST /api/rewriter/generate-scorecard
Body: { analysis, interview_summary, candidate_name }
Response: PDF file (application/pdf)
⏱️ 1-2 seconds
```

---

## 🔐 Security Flow

```
1. User uploads resume → Frontend
   ↓
2. Resume stored in memory only (not disk)
   ↓
3. PDF text extracted → Sent to backend
   ↓
4. Backend sends to Cerebras AI
   ↓
5. AI processes and returns
   ↓
6. Backend formats response
   ↓
7. Frontend displays
   ↓
8. User closes browser → All data cleared
   ❌ No persistence, no storage
```

---

## 📈 Performance Optimization

### Backend
- Async FastAPI endpoints
- Efficient PDF parsing
- Cached responses (optional)
- Connection pooling

### Frontend
- Component lazy loading
- Optimized re-renders
- Efficient state updates
- Debounced API calls

### AI
- Optimized prompts
- Temperature tuning
- Token limit management
- Error retry logic

---

## 🎨 Component Hierarchy

```
App.jsx
├── Header (navigation, branding)
├── TabNavigation (3 tabs)
├── Main Content
│   ├── [Tab 1: Analysis]
│   │   ├── ResumeUpload
│   │   │   ├── PDF Upload Input
│   │   │   └── JD Textarea
│   │   └── AIAnalysis
│   │       ├── Score Display
│   │       ├── Download PDF Button
│   │       ├── Why Not Passing
│   │       ├── Missing Keywords
│   │       ├── Gap Analysis
│   │       ├── Section Feedback
│   │       ├── Action Plan
│   │       └── Start Interview Button
│   │
│   ├── [Tab 2: Interview]
│   │   └── AIInterviewer
│   │       ├── Welcome Message
│   │       ├── Chat Messages
│   │       │   ├── AI Questions
│   │       │   ├── User Answers
│   │       │   └── STAR Feedback
│   │       ├── Answer Input
│   │       └── Summary Display
│   │
│   └── [Tab 3: Rewriter]
│       └── StarRewriter
│           ├── STAR Framework Info
│           ├── Bullet Input
│           ├── Rewrite Button
│           └── Results Display
│               ├── Before/After
│               ├── STAR Breakdown
│               ├── Impact Score
│               └── Keywords Added
│
└── Footer
```

---

**This architecture ensures:**
- 🔒 Security through no-persistence design
- ⚡ Performance through async operations
- 🎯 Scalability through modular architecture
- 🧪 Testability through clear separation
- 📱 Responsiveness through modern CSS
- ♿ Accessibility through semantic HTML

---

*System designed and implemented December 24, 2025*
