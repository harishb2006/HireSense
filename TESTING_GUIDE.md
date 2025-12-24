# 🧪 HireSense - Complete Testing Guide

## Quick Start

### 1. Setup (First Time Only)
```bash
./setup.sh
```

### 2. Configure API Key
```bash
cd backend
nano .env  # or use your favorite editor
# Add: CEREBRAS_API_KEY=your-actual-api-key-here
```

### 3. Start Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Start Frontend (New Terminal)
```bash
cd frontend
npm run dev
```

### 5. Access Application
Open http://localhost:5173

---

## 🎯 Complete Feature Testing Workflow

### Phase 1: Resume Analysis Testing

#### Test Case 1: Basic Upload & Analysis
1. **Navigate to** Resume Analysis tab (should be default)
2. **Upload** a sample PDF resume
3. **Paste** a job description in the text area
4. **Click** "Analyze Resume with AI"
5. **Expected Results:**
   - Loading indicator appears
   - Analysis completes within 10-30 seconds
   - Match score displayed (0-100%)
   - Color coding: Green (70+), Orange (50-70), Red (<50)
   - "Why Not Passing" section with 3+ reasons
   - Missing Keywords table with importance levels
   - Gap Analysis sections
   - Section-by-Section Feedback
   - Action Plan steps

#### Test Case 2: Download PDF Scorecard
1. **After analysis**, locate "Download PDF Scorecard" button
2. **Click** the button
3. **Expected Results:**
   - Loading indicator on button
   - PDF downloads automatically
   - Filename: `HireSense_Scorecard_Candidate_YYYY-MM-DD.pdf`
   - PDF contains:
     - Match score with visual indicators
     - Key issues table
     - Missing keywords table
     - Recommended actions
     - Professional formatting with colors

#### Test Case 3: Score Variations
Test with different resume-JD combinations:

**Low Match (Expected 20-40%)**
- Resume: Generic software engineer
- JD: Senior DevOps with AWS/K8s requirements
- Should show many missing keywords and critical gaps

**Medium Match (Expected 50-70%)**
- Resume: Junior developer with some relevant skills
- JD: Mid-level role with moderate requirements
- Should show moderate gaps with improvement suggestions

**High Match (Expected 75-95%)**
- Resume: Senior engineer with all required skills
- JD: Role matching candidate's exact profile
- Should show minimal gaps, mostly optimization suggestions

### Phase 2: Mock Interview Testing

#### Test Case 4: Interview Question Generation
1. **After analysis**, click "Start Mock Interview" button
2. **Expected Results:**
   - Navigate to Interview tab
   - Welcome message from AI
   - First question appears automatically
   - Question is relevant to missing skills/weak areas
   - Question metadata visible (category, focus area)

#### Test Case 5: Answer Evaluation
1. **Type an answer** in the text box
2. **Submit** the answer
3. **Expected Results:**
   - Answer appears in chat
   - AI evaluates using STAR framework
   - Feedback includes:
     - Score (0-100%)
     - STAR analysis (Situation, Task, Action, Result)
     - Strengths (2-3 points)
     - Improvements (2-3 points)
     - Suggestion for better answer
     - Example reframe

#### Test Case 6: STAR Framework Scoring
Test different answer qualities:

**Poor Answer (Expected score: 30-50%)**
```
I worked on a project. It was good.
```
- Should flag missing STAR components
- Suggest adding context, actions, results

**Medium Answer (Expected score: 60-75%)**
```
When I was at Company X, we needed to improve performance. 
I optimized the database queries. The system became faster.
```
- Should recognize partial STAR structure
- Suggest quantifying results

**Excellent Answer (Expected score: 85-100%)**
```
At Company X, our API response time was 2 seconds, causing customer complaints (S). 
I was tasked with reducing latency by 50% within 2 weeks (T). 
I profiled the system, identified N+1 queries, implemented Redis caching, 
and optimized database indexes (A). 
This reduced response time to 400ms (80% improvement), 
increased user satisfaction from 3.2 to 4.5/5, and reduced server costs by 30% (R).
```
- Should score very high
- Recognize all STAR components
- Praise quantifiable metrics

#### Test Case 7: Complete Interview
1. **Answer all questions** (typically 5 questions)
2. **Expected Results:**
   - Interview completion message
   - Overall performance summary:
     - Overall score (average of all answers)
     - Performance level (Excellent/Good/Needs Improvement)
     - Key strengths (3-4 points)
     - Areas for improvement (3-4 points)
     - Recommendations (4-5 action items)
     - Next steps

### Phase 3: STAR Rewriter Testing

#### Test Case 8: Basic Bullet Rewrite
1. **Navigate to** STAR Rewriter tab
2. **Enter a weak bullet:**
   ```
   Worked on team project
   ```
3. **Click** "Rewrite with STAR Framework"
4. **Expected Results:**
   - Loading indicator
   - Before/After comparison displayed
   - Before section shows original with issues highlighted
   - After section shows improved version
   - STAR breakdown showing each component
   - Impact score improvement (+40-80%)
   - Keywords added list
   - Copy button functional

#### Test Case 9: Different Bullet Types
Test various bullet weaknesses:

**Task-focused (no impact)**
```
Managed team meetings and coordinated schedules
```
Expected improvement: Add leadership metrics, outcomes

**Too vague**
```
Improved system performance
```
Expected improvement: Add specific technologies, quantifiable results

**Already good (minimal changes)**
```
Led team of 5 engineers to deliver microservices platform, 
reducing deployment time by 60% and supporting 1M+ daily users
```
Expected improvement: Minor optimizations, keyword additions

#### Test Case 10: Copy Functionality
1. **After rewrite**, click copy icon on improved version
2. **Paste** in a text editor
3. **Expected Results:**
   - Exact improved text copied
   - No formatting issues
   - Ready for resume update

### Phase 4: End-to-End Workflow

#### Test Case 11: Complete User Journey
1. **Upload** resume + JD
2. **Review** analysis results
3. **Download** PDF scorecard
4. **Start** mock interview
5. **Complete** 5 interview questions
6. **Download** updated PDF with interview results
7. **Navigate to** STAR Rewriter
8. **Rewrite** 2-3 weak bullets
9. **Re-analyze** updated resume (optional)
10. **Compare** before/after scores

**Expected Total Time:** 15-20 minutes

---

## 🔧 Backend API Testing

### Using cURL

#### Test Analysis Endpoint
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Software Engineer with 3 years experience in Python...",
    "job_description": "Senior DevOps Engineer with AWS and Kubernetes..."
  }'
```

#### Test STAR Rewriter
```bash
curl -X POST http://localhost:8000/api/rewriter/star-rewrite \
  -H "Content-Type: application/json" \
  -d '{
    "original_bullet": "Worked on team project",
    "job_description": "Senior Software Engineer role...",
    "resume_context": "Software Engineer at Company X..."
  }'
```

#### Test PDF Generation
```bash
curl -X POST http://localhost:8000/api/rewriter/generate-scorecard \
  -H "Content-Type: application/json" \
  -d @analysis_result.json \
  --output scorecard.pdf
```

### Using Swagger UI
Navigate to http://localhost:8000/docs for interactive API documentation

---

## 🐛 Common Issues & Solutions

### Issue 1: Backend fails to start
**Error:** `ModuleNotFoundError: No module named 'cerebras'`
**Solution:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Issue 2: PDF download fails
**Error:** `Failed to generate PDF`
**Solution:**
```bash
pip install reportlab==4.0.7
```

### Issue 3: Frontend won't connect to backend
**Error:** `Failed to fetch`
**Solution:**
1. Check backend is running: http://localhost:8000
2. Check CORS settings in backend/main.py
3. Verify frontend is using correct API URL

### Issue 4: LLM returns mock data
**Warning:** `Using mock response`
**Solution:**
1. Check `.env` file has valid `CEREBRAS_API_KEY`
2. Verify API key at https://cerebras.ai/
3. Check internet connection

### Issue 5: Analysis takes too long
**Expected:** 10-30 seconds
**If longer:**
1. Check Cerebras API status
2. Try shorter resume/JD text
3. Check server logs for errors

---

## 📊 Performance Benchmarks

### Expected Response Times
| Operation | Expected Time | Max Acceptable |
|-----------|--------------|----------------|
| Resume Analysis | 5-15s | 30s |
| Question Generation | 3-8s | 15s |
| Answer Evaluation | 2-5s | 10s |
| STAR Rewrite | 3-7s | 15s |
| PDF Generation | 1-2s | 5s |

### Expected Accuracy
| Metric | Target | Good | Excellent |
|--------|--------|------|-----------|
| Keyword Detection | 80% | 85% | 90%+ |
| Gap Identification | 75% | 80% | 85%+ |
| STAR Scoring | 70% | 80% | 85%+ |
| Question Relevance | 80% | 90% | 95%+ |

---

## 🎯 Test Data Samples

### Sample Resume (Low Match)
```
John Doe
Software Engineer

Skills: HTML, CSS, JavaScript, jQuery

Experience:
- Built websites for clients
- Fixed bugs in legacy code
- Worked with team on projects
```

### Sample Job Description (DevOps)
```
Senior DevOps Engineer

Requirements:
- 5+ years DevOps experience
- Expert in Docker, Kubernetes, AWS
- CI/CD pipeline design and implementation
- Infrastructure as Code (Terraform)
- Monitoring and logging (Prometheus, Grafana)
- Python/Go scripting
```

**Expected Match Score:** 15-25%
**Expected Missing Keywords:** Docker, Kubernetes, AWS, CI/CD, Terraform, DevOps

---

## ✅ Test Checklist

### Resume Analysis
- [ ] Upload PDF successfully
- [ ] Paste job description
- [ ] Receive match score (0-100)
- [ ] See missing keywords
- [ ] View gap analysis
- [ ] Read section feedback
- [ ] Review action steps
- [ ] Download PDF scorecard

### Mock Interview
- [ ] Navigate to interview tab
- [ ] See welcome message
- [ ] Receive first question
- [ ] Submit answer
- [ ] Receive STAR evaluation
- [ ] See feedback with score
- [ ] Complete all questions
- [ ] View performance summary
- [ ] Download complete PDF

### STAR Rewriter
- [ ] Navigate to rewriter tab
- [ ] Enter weak bullet
- [ ] Receive improved version
- [ ] See before/after comparison
- [ ] View STAR breakdown
- [ ] See impact improvement
- [ ] Copy improved text
- [ ] Rewrite multiple bullets

### Cross-Feature
- [ ] Tab navigation works
- [ ] Data persists across tabs
- [ ] PDF includes all information
- [ ] UI is responsive
- [ ] No console errors
- [ ] Proper error handling

---

## 🚀 Ready to Test!

1. Run `./setup.sh` if first time
2. Start backend and frontend
3. Open http://localhost:5173
4. Follow test cases above
5. Report issues with details:
   - Steps to reproduce
   - Expected vs actual results
   - Console errors
   - Screenshots

**Happy Testing! 🎉**
