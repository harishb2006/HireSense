# Prep Pro - Dynamic AI Interview Simulator

## 🚀 Overview

Prep Pro is a state-aware AI interviewer that provides realistic technical interview practice with **multi-turn conversation memory**, **adaptive questioning**, and **real-time evaluation**. Unlike static question banks, Prep Pro remembers your responses and adapts its questions based on your performance.

## ✨ Key Features

### 1. **Multi-turn Conversation State**
- AI remembers everything you said during the interview
- Maintains context across 10-minute sessions
- Uses conversation history to generate relevant follow-up questions

### 2. **Adaptive Questioning System**
- **Depth Detection**: Analyzes technical depth of your answers (0-10 scale)
- **Smart Follow-ups**: If you give shallow answers, AI drills down with specific questions
- **Dynamic Topics**: Smoothly transitions between topics based on your performance
- **No Repetition**: Each question builds on previous ones

### 3. **Live Evaluation Engine**
Real-time scoring across three dimensions:
- **Technical Depth**: Use of technical terms, explanations, code examples
- **Clarity**: Structure, logical flow, readability
- **Confidence**: Assertive language vs. hedging words

### 4. **Knowledge Map (Weakness Detection)**
After the interview, get a visual breakdown:
```json
{
  "Event Loop": {
    "average_score": 7.5,
    "assessment": "Moderate",
    "strong_areas": ["Async I/O", "Callbacks"],
    "weak_areas": ["Microtask queue", "setImmediate"]
  },
  "Database": {
    "average_score": 4.2,
    "assessment": "Needs Improvement",
    "strong_areas": ["Basic queries"],
    "weak_areas": ["Indexing", "Transactions", "Normalization"]
  }
}
```

### 5. **Comprehensive Debrief Report**
- Side-by-side comparison: Your answers vs. Model answers
- Transcript with timestamps and scores
- Personalized improvement recommendations
- Performance trend analysis (improving/declining/consistent)

### 6. **Voice Mode (Experimental)**
- Speak your answers instead of typing
- AI speaks questions aloud using Text-to-Speech
- Uses Web Speech API (Chrome/Edge)

## 🎯 How It Works

### User Workflow

1. **Setup**:
   - Enter name and email
   - Select role (Node.js, React, Python, etc.)
   - Choose seniority level (Junior, Mid, Senior)
   - Optional: Enable voice mode

2. **Interview**:
   ```
   AI: "Can you explain how the Event Loop handles Asynchronous I/O?"
   
   You: "The event loop checks queues for callbacks..."
   
   [AI analyzes depth = 5/10 - shallow answer]
   
   AI: "You mentioned the Poll phase; what happens if a setImmediate 
        is scheduled during that time?" [DRILL-DOWN QUESTION]
   ```

3. **Live Scoring**:
   - See your scores update in real-time
   - Current topic displayed at top
   - Follow-up questions are marked with a badge

4. **Completion** (10 minutes or 10 questions):
   - View detailed HTML report
   - Check knowledge map
   - Get personalized study recommendations

## 🏗️ Architecture

### Backend Services

#### 1. `AIInterviewer` (services/ai_interviewer.py)
- Generates opening questions dynamically
- Analyzes answer depth using Gemini AI
- Generates adaptive follow-up questions
- Maintains conversation state (topics covered, knowledge map)
- Determines when to end interview

Key Methods:
```python
generate_opening_question(topics) → question + topic + ideal_answer
analyze_answer_depth(question, user_answer, ideal_answer) → scores + gaps
generate_follow_up_question(previous_q, answer, analysis) → drill-down question
get_knowledge_map() → strengths/weaknesses breakdown
```

#### 2. `LiveEvaluator` (services/live_evaluator.py)
- Evaluates responses in real-time (no delays)
- Uses rule-based scoring + pattern matching
- Tracks cumulative scores across session
- Provides performance trend analysis

Scoring Logic:
- **Technical Depth**: Keywords, code examples, explanations
- **Clarity**: Structure, sentences, connectors
- **Confidence**: Assertive vs. uncertain language

#### 3. `InterviewAnalyzer` (services/interview_analyzer.py)
- Generates post-interview debrief reports
- Compares user answers to model answers
- Creates HTML reports with visualizations
- Suggests personalized study resources

### Database Schema

**interview_sessions**:
```sql
- ai_context JSONB           -- AI's memory of user's abilities
- follow_up_queue JSONB      -- Queue of potential follow-ups
- knowledge_map JSONB        -- Topic → score mapping
- current_topic VARCHAR      -- Active discussion topic
- topics_covered TEXT[]      -- Completed topics
```

**conversation_messages**:
```sql
- is_follow_up VARCHAR       -- 'true' if drill-down question
- topic VARCHAR              -- Message topic category
- keywords_detected TEXT[]   -- Technical terms found
- model_answer TEXT          -- Ideal answer for comparison
```

### API Endpoints

#### Start Interview
```http
POST /api/mock-interview/start
{
  "user_name": "John Doe",
  "user_email": "john@example.com",
  "role": "Node.js Developer",
  "seniority_level": "Senior"
}

Response:
{
  "session_id": "uuid",
  "first_question": "Can you explain...",
  "message_number": 1
}
```

#### Submit Answer
```http
POST /api/mock-interview/answer
{
  "session_id": "uuid",
  "answer": "User's response text"
}

Response:
{
  "next_question": "Follow-up or new question",
  "depth_score": 7.5,
  "clarity_score": 8.0,
  "confidence_score": 6.5,
  "overall_score": 7.3,
  "is_follow_up": true,
  "current_topic": "Event Loop",
  "session_status": "active"
}
```

#### Get Knowledge Map
```http
GET /api/mock-interview/session/{session_id}/knowledge-map

Response:
{
  "knowledge_map": {
    "Event Loop": {
      "average_score": 7.5,
      "assessment": "Moderate",
      "strong_areas": [...],
      "weak_areas": [...]
    }
  }
}
```

#### Get Debrief Report
```http
GET /api/mock-interview/session/{session_id}/report
GET /api/mock-interview/session/{session_id}/report/html
```

## 🧠 AI Prompting Strategy

### Opening Question Generation
```
"You are an expert technical interviewer for a {seniority} {role}.
Generate a compelling opening question that:
1. Tests fundamental understanding
2. Allows for both breadth and depth
3. Focuses on: {available_topics}

Return JSON: {question, topic, ideal_answer, key_concepts, follow_up_hints}"
```

### Answer Depth Analysis
```
"Analyze this candidate's answer:
QUESTION: {question}
USER'S ANSWER: {answer}
IDEAL ANSWER: {ideal}

Provide:
1. Technical Depth Score (0-10)
2. Missing Key Concepts
3. Strong Points
4. Needs Follow-up? (true/false)

Return JSON: {scores, missing_concepts, strong_points, needs_follow_up}"
```

### Follow-up Generation
```
"PREVIOUS QUESTION: {question}
USER'S ANSWER: {answer}
ANALYSIS: Scored {score}/10, missing {concepts}

STRATEGY: {dig_deeper | advance | test_fundamentals}

Generate a follow-up that:
1. Naturally continues conversation
2. Tests deeper understanding of weak areas
3. Is not repetitive"
```

## 🔧 Configuration

### Environment Variables
```bash
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:pass@localhost:5433/hiresense_db
```

### Customization

**Interview Duration**:
```python
# services/ai_interviewer.py
def should_end_interview(duration_minutes, questions_asked):
    if duration_minutes >= 10:  # Change this
        return True
```

**Scoring Weights**:
```python
# services/live_evaluator.py
def _evaluate_technical_depth(answer):
    score = 5.0  # Base score
    score += min(technical_count * 0.3, 3.0)  # Adjust multipliers
```

## 📊 Metrics & Analytics

The system tracks:
- **Session Duration**: Actual time spent
- **Questions Asked**: Total Q&A pairs
- **Topics Covered**: Breadth of discussion
- **Performance Trend**: Improving/Declining/Consistent
- **Knowledge Gaps**: Specific weak areas

## 🚀 Getting Started

1. **Database Setup**:
   ```bash
   docker-compose up -d
   cd backend
   PGPASSWORD=hiresense_password psql -h localhost -p 5433 -U hiresense_user -d hiresense_db -f database/init.sql
   ```

2. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   export GEMINI_API_KEY=your_key
   uvicorn main:app --reload
   ```

3. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access**: http://localhost:5173

## 🎨 Frontend Features

### Live Scoring Display
Real-time score cards showing:
- Technical Depth
- Clarity
- Confidence
- Overall Score

### Chat Interface
- Smooth message animations
- Typing indicators
- Follow-up badges
- Timestamp tracking

### Voice Mode
- 🎤 Voice input button
- Auto-transcription
- Text-to-Speech for questions

## 🔮 Future Enhancements

### Planned Features:
1. **Video Recording**: Record interview for playback
2. **Peer Comparison**: Compare scores with others at your level
3. **Topic Selection**: Choose specific topics to practice
4. **Company-Specific**: Prep for specific company styles (Google, Amazon, etc.)
5. **Mock Coding**: Integrate code editor for live coding questions
6. **Resume Integration**: Generate questions from your actual resume
7. **Spaced Repetition**: Schedule follow-up sessions on weak topics

### AI Improvements:
- Fine-tune models on real interview data
- Better detection of non-technical skills (communication, problem-solving)
- Multi-language support
- Emotion/stress detection (via voice analysis)

## 📝 Example Interview Session

```
[Setup: Senior Node.js Developer]

AI: "Can you explain how the Event Loop handles Asynchronous I/O in Node.js?"

User: "The event loop checks for callbacks in different phases."
[Depth: 4/10 - Too vague]

AI: "You mentioned phases. Can you describe what happens in the Poll phase specifically?"
[FOLLOW-UP QUESTION]

User: "The poll phase retrieves new I/O events and executes I/O related callbacks..."
[Depth: 7/10 - Better!]

AI: "Good! Now, what's the difference between setImmediate and setTimeout(fn, 0)?"
[NEW CHALLENGING QUESTION]

User: "setImmediate runs in the check phase after poll, while setTimeout..."
[Depth: 8/10 - Strong answer]

AI: "Excellent explanation. Let's move to another topic. Can you explain how you'd design a rate limiter?"
[TOPIC TRANSITION]
```

## 🤝 Contributing

To add new question categories:
1. Add to `database/init.sql`
2. Update topic lists in `AIInterviewer`
3. Add scoring patterns in `LiveEvaluator`

## 📄 License

MIT License

---

**Built with ❤️ using FastAPI, React, PostgreSQL, and Google Gemini AI**
