import json
import os
from typing import Dict, Any, List
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIAnalyzer:
    """
    AI-powered resume analysis service using Cerebras AI
    Returns structured JSON output for resume analysis
    """
    
    def __init__(self):
        # Load API key from environment variables
        self.api_key = os.getenv("CEREBRAS_API_KEY", "")
        self.model = os.getenv("CEREBRAS_MODEL", "llama-3.3-70b")
        
        # Initialize Cerebras client if API key exists
        self.client = None
        if self.api_key and self.api_key != "your-cerebras-api-key-here":
            try:
                self.client = Cerebras(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize Cerebras client: {e}")
                self.client = None
        
    def analyze_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Analyze resume against job description using AI
        Returns structured JSON output
        
        Args:
            resume_text: Extracted text from resume
            job_description: Job description text
            
        Returns:
            Structured analysis with match_score, missing_keywords, and section_feedback
        """
        
        system_prompt, user_prompt = self._build_analysis_prompt(resume_text, job_description)
        
        # Call LLM with proper prompts
        analysis = self._call_llm(system_prompt, user_prompt)
        
        return analysis
    
    def _build_analysis_prompt(self, resume_text: str, job_description: str) -> str:
        """
        Build the system and user prompts for LLM analysis
        Returns tuple of (system_prompt, user_prompt)
        """
        
        system_prompt = """You are an expert career mentor and ATS specialist with 15+ years of experience in recruitment and career development.

Your role is to act as a MENTOR, not just a scanner. When a resume doesn't pass, you must explain WHY it's failing and WHAT the candidate needs to understand about the gap between their profile and the job requirements.

You MUST return ONLY a valid JSON object with no additional text, explanations, or markdown formatting.

The JSON must follow this exact structure:
{
  "match_score": <number between 0-100>,
  "overall_assessment": "<2-3 sentences explaining if this resume would pass ATS screening and why/why not>",
  "why_not_passing": {
    "main_reasons": [
      "<Reason 1: Explain what's fundamentally wrong>",
      "<Reason 2: Another critical issue>",
      "<Reason 3: etc.>"
    ],
    "ats_perspective": "<Explain how an ATS system would view this resume - what it's looking for and what it's not finding>"
  },
  "missing_keywords": [
    {
      "keyword": "<missing keyword/skill>",
      "importance": "<critical/high/medium>",
      "why_matters": "<Explain WHY this keyword is important for this role and what impact its absence has>"
    }
  ],
  "gap_analysis": {
    "experience_gaps": "<Detailed explanation of experience mismatches - what the JD needs vs what the resume shows>",
    "skills_gaps": "<Detailed explanation of technical/soft skill gaps and their significance>",
    "qualification_gaps": "<Education, certifications, or other qualification gaps>"
  },
  "section_detailed_feedback": {
    "summary": {
      "current_state": "<What's currently there or missing>",
      "problem": "<Why it's not working for this role>",
      "impact": "<How this affects ATS screening>"
    },
    "experience": {
      "current_state": "<What's currently there>",
      "problem": "<Why it's not aligning with job requirements>",
      "impact": "<How this affects candidacy>"
    },
    "skills": {
      "current_state": "<What skills are listed>",
      "problem": "<What's missing or not emphasized>",
      "impact": "<How this affects technical screening>"
    }
  },
  "actionable_next_steps": [
    "<Step 1: Most critical action to take>",
    "<Step 2: Next important action>",
    "<Step 3: etc.>"
  ]
}

IMPORTANT RULES:
1. Be BRUTALLY HONEST but CONSTRUCTIVE - explain the real problems
2. Think like an ATS system first, then like a hiring manager
3. Explain WHY things matter, not just WHAT is missing
4. Focus on the GAPS - what's preventing this resume from passing
5. Provide clear, actionable explanations that help the candidate understand their weaknesses
6. Match score should reflect realistic ATS pass rate (typically 60+ to pass initial screening)
7. Use mentoring language - teach, don't just critique"""

        user_prompt = f"""Analyze this resume as a MENTOR explaining why it may not pass the ATS screening:

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Provide a comprehensive analysis that:
1. Explains if this resume would pass ATS screening (match_score)
2. Details WHY it's not passing or what's holding it back
3. Identifies missing critical keywords with explanations of their importance
4. Analyzes the gaps between candidate profile and job requirements
5. Gives detailed feedback for each resume section with current state, problem, and impact
6. Provides actionable next steps

Return ONLY the JSON object following the exact structure above."""

        return system_prompt, user_prompt
    
    def _call_llm(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Call Cerebras AI API and parse JSON response
        Falls back to mock data if API key not configured
        """
        
        # If Cerebras client is configured, use it
        if self.client:
            try:
                print("🤖 Calling Cerebras AI API...")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_completion_tokens=2048,
                    temperature=0.2,
                    top_p=1,
                    stream=False
                )
                
                # Parse the JSON response
                content = response.choices[0].message.content
                print(f"✅ Received response ({len(content)} chars)")
                
                # Try to extract JSON if wrapped in markdown
                if "```json" in content:
                    print("⚠️  Response contains markdown, extracting JSON...")
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    print("⚠️  Response contains code blocks, extracting content...")
                    content = content.split("```")[1].split("```")[0].strip()
                
                analysis = json.loads(content)
                print(f"✅ Successfully parsed JSON with keys: {list(analysis.keys())}")
                
                return analysis
                
            except json.JSONDecodeError as e:
                print(f"❌ Error: Failed to parse JSON from Cerebras response: {e}")
                print(f"Response preview: {content[:500]}...")
                print("⚠️  Falling back to mock response")
                return self._get_mock_response()
            except Exception as e:
                print(f"❌ Error calling Cerebras AI API: {type(e).__name__}: {e}")
                print("⚠️  Falling back to mock response")
                return self._get_mock_response()
        
        # Fall back to mock response if no API key
        print("⚠️  Warning: Using mock response. Set CEREBRAS_API_KEY in .env file to use real AI analysis")
        return self._get_mock_response()
    
    def _get_mock_response(self) -> Dict[str, Any]:
        """
        Return mock response for development/testing with enhanced mentor-style feedback
        """
        mock_response = {
            "match_score": 45,
            "overall_assessment": "This resume would likely NOT pass initial ATS screening. The match score of 45% indicates significant gaps in technical keywords, relevant experience presentation, and alignment with the job requirements.",
            "why_not_passing": {
                "main_reasons": [
                    "Missing critical cloud infrastructure keywords that are essential for this role (Docker, Kubernetes, AWS services)",
                    "Experience descriptions don't emphasize scalability, distributed systems, or microservices architecture",
                    "No clear demonstration of DevOps practices or CI/CD pipeline experience"
                ],
                "ats_perspective": "ATS systems scan for exact keyword matches and semantic relevance. This resume lacks 60% of the critical technical terms from the job description. The system would flag it as 'underqualified' because key technologies (containerization, orchestration, cloud platforms) are either absent or not prominently featured."
            },
            "missing_keywords": [
                {
                    "keyword": "Docker",
                    "importance": "critical",
                    "why_matters": "Docker containerization is fundamental to modern DevOps practices. Its absence suggests you may not have hands-on experience with containerized deployments, which is a dealbreaker for this role."
                },
                {
                    "keyword": "Kubernetes",
                    "importance": "critical",
                    "why_matters": "Kubernetes orchestration is explicitly mentioned as a required skill. Without it, the hiring team will assume you can't manage production-scale containerized applications."
                },
                {
                    "keyword": "Microservices Architecture",
                    "importance": "high",
                    "why_matters": "The role requires designing and maintaining microservices. Not mentioning this suggests you may have only monolithic application experience, which doesn't meet the job's architectural needs."
                },
                {
                    "keyword": "CI/CD Pipeline",
                    "importance": "high",
                    "why_matters": "Continuous integration and deployment is core to the DevOps workflow. Its absence indicates you might not be familiar with automated testing and deployment processes."
                },
                {
                    "keyword": "AWS (Lambda, ECS, ECR)",
                    "importance": "critical",
                    "why_matters": "The company's infrastructure is AWS-based. Not showcasing specific AWS services means you'll need extensive onboarding, which they want to avoid."
                }
            ],
            "gap_analysis": {
                "experience_gaps": "The job requires 3-5 years of DevOps experience with proven track record in cloud infrastructure. Your resume shows software development experience but doesn't clearly articulate infrastructure management, monitoring, or deployment automation responsibilities. Hiring managers need to see specific examples of infrastructure you've built, scaled, or maintained.",
                "skills_gaps": "Critical technical gaps: No container orchestration tools mentioned, no infrastructure-as-code experience (Terraform, CloudFormation), no monitoring tools (Prometheus, Grafana). The job emphasizes these as day-1 requirements, and their absence suggests a fundamental skills mismatch.",
                "qualification_gaps": "While you have a CS degree, there's no mention of relevant certifications (AWS Certified Solutions Architect, Kubernetes Admin) that would validate your cloud expertise. For senior roles, certifications help compensate for experience gaps."
            },
            "section_detailed_feedback": {
                "summary": {
                    "current_state": "Generic software engineer summary focusing on 'problem-solving' and 'team collaboration' without technical depth",
                    "problem": "Doesn't position you as a DevOps/Cloud specialist. The summary should immediately signal your cloud infrastructure expertise and mention 2-3 of the critical technologies from the JD",
                    "impact": "ATS scores summaries heavily. A generic summary means you're competing as a 'generalist' when this role needs a 'specialist'. This alone could drop your score by 15-20 points."
                },
                "experience": {
                    "current_state": "Experience bullets focus on feature development and team coordination but lack infrastructure/deployment specifics",
                    "problem": "Job descriptions emphasize WHAT you built (infrastructure, pipelines, monitoring systems) not just development work. Your bullets don't show you've operated in a DevOps capacity",
                    "impact": "Hiring managers will question if you've actually done the infrastructure work they need. Without deployment and scaling examples, you seem like a developer, not a DevOps engineer."
                },
                "skills": {
                    "current_state": "Skills list includes programming languages (Python, JavaScript) but minimal DevOps tools",
                    "problem": "The skills section is where ATS does heavy keyword matching. You're missing 8+ critical keywords: Docker, K8s, Terraform, Jenkins, GitLab CI, CloudFormation, AWS services, monitoring tools",
                    "impact": "ATS systems weight skills section at 40-50% of total score. Your current skills profile matches maybe 30% of requirements, significantly lowering your overall match score."
                }
            },
            "actionable_next_steps": [
                "IMMEDIATE: Add a 'Cloud & DevOps Technologies' section listing: Docker, Kubernetes, AWS (EC2, ECS, Lambda, S3, RDS), CI/CD tools, Infrastructure as Code tools",
                "REWRITE SUMMARY: Position yourself as 'DevOps Engineer with X years cloud infrastructure experience' and mention 3 key technologies from the JD in the first line",
                "REVISE EXPERIENCE BULLETS: For each role, add 2-3 bullets specifically about infrastructure work - deployments, automation, scaling, monitoring. Use metrics (reduced deployment time by X%, managed infrastructure for Y users)",
                "ADD PROJECTS SECTION: If lacking professional DevOps experience, include personal projects showing Docker/K8s/AWS work. Even side projects demonstrate capability.",
                "GET CERTIFIED: Consider AWS Solutions Architect Associate or CKA (Certified Kubernetes Administrator) certification to validate your cloud skills"
            ]
        }
        
        return mock_response
    
    def validate_analysis_output(self, analysis: Dict[str, Any]) -> bool:
        """
        Validate that the analysis output matches expected mentor-style schema
        """
        required_fields = [
            "match_score", 
            "overall_assessment",
            "why_not_passing",
            "missing_keywords",
            "gap_analysis",
            "section_detailed_feedback",
            "actionable_next_steps"
        ]
        
        # Check all required top-level fields exist
        if not all(field in analysis for field in required_fields):
            print(f"Missing required fields. Present: {list(analysis.keys())}")
            return False
        
        # Validate match_score
        if not isinstance(analysis["match_score"], (int, float)):
            print("Invalid match_score type")
            return False
        
        # Validate overall_assessment
        if not isinstance(analysis["overall_assessment"], str):
            print("Invalid overall_assessment type")
            return False
        
        # Validate why_not_passing structure
        if not isinstance(analysis["why_not_passing"], dict):
            print("Invalid why_not_passing type")
            return False
        
        # Validate missing_keywords (array of objects)
        if not isinstance(analysis["missing_keywords"], list):
            print("Invalid missing_keywords type")
            return False
        
        # Validate gap_analysis
        if not isinstance(analysis["gap_analysis"], dict):
            print("Invalid gap_analysis type")
            return False
        
        # Validate section_detailed_feedback
        if not isinstance(analysis["section_detailed_feedback"], dict):
            print("Invalid section_detailed_feedback type")
            return False
        
        # Validate actionable_next_steps
        if not isinstance(analysis["actionable_next_steps"], list):
            print("Invalid actionable_next_steps type")
            return False
        
        return True
    
    def generate_interview_questions(
        self, 
        resume_text: str, 
        job_description: str, 
        analysis: Dict[str, Any],
        count: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate targeted interview questions based on analysis
        Focuses on weak areas and missing skills
        """
        
        missing_keywords = analysis.get("missing_keywords", [])[:5]
        gap_analysis = analysis.get("gap_analysis", {})
        
        system_prompt = """You are an experienced technical recruiter conducting a mock interview.
Your goal is to ask questions that specifically target the candidate's WEAK AREAS and MISSING SKILLS identified in their resume analysis.

Generate interview questions that:
1. Test knowledge in areas where the candidate is weak
2. Allow the candidate to demonstrate understanding of missing concepts
3. Are realistic questions a hiring manager would ask for this role
4. Mix technical, behavioral, and situational questions
5. Help the candidate practice explaining gaps in their experience

Return ONLY a JSON array of question objects:
[
  {
    "question": "<the interview question>",
    "category": "technical|behavioral|situational",
    "focus_area": "<which weakness/gap this targets>",
    "why_asking": "<brief explanation of why this question matters for this role>"
  }
]"""

        user_prompt = f"""Based on this analysis, generate {count} targeted interview questions:

JOB DESCRIPTION:
{job_description}

CANDIDATE'S WEAK AREAS:
Missing Keywords: {', '.join([k.get('keyword', '') for k in missing_keywords])}
Experience Gaps: {gap_analysis.get('experience_gaps', 'None identified')}
Skills Gaps: {gap_analysis.get('skills_gaps', 'None identified')}

RESUME SUMMARY:
{resume_text[:500]}...

Generate {count} questions that will help the candidate:
1. Practice explaining their experience in the context of missing skills
2. Demonstrate problem-solving in areas they're weak
3. Show transferable skills that could compensate for gaps

Return ONLY the JSON array of question objects."""

        try:
            if self.client:
                print("🤖 Generating interview questions with AI...")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.8,
                    max_tokens=2000
                )
                
                content = response.choices[0].message.content.strip()
                print(f"✅ Received {len(content)} chars from AI")
                content = content.replace("```json", "").replace("```", "").strip()
                questions = json.loads(content)
                
                if isinstance(questions, list) and len(questions) > 0:
                    print(f"✅ Generated {len(questions)} questions")
                    return questions
            else:
                print("⚠️  No AI client configured, using fallback questions")
        except Exception as e:
            print(f"❌ AI question generation error: {e}")
            print("⚠️  Falling back to template questions")
        
        # Fallback: Generate questions based on missing keywords
        return self._generate_fallback_questions(missing_keywords, gap_analysis, count)
    
    def _generate_fallback_questions(
        self,
        missing_keywords: List[Dict[str, Any]],
        gap_analysis: Dict[str, Any],
        count: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate fallback interview questions when AI is unavailable
        """
        questions = []
        
        # Technical questions based on missing keywords
        for i, keyword_obj in enumerate(missing_keywords[:min(3, count)]):
            keyword = keyword_obj.get('keyword', 'technical skill')
            questions.append({
                "question": f"Can you describe your experience with {keyword}? How have you applied it in your previous projects?",
                "category": "technical",
                "focus_area": keyword,
                "why_asking": f"This role requires proficiency in {keyword}, which wasn't clearly evident in your resume."
            })
        
        # Behavioral question about experience gaps
        if gap_analysis.get('experience_gaps') and len(questions) < count:
            questions.append({
                "question": "Tell me about a time when you had to quickly learn a new technology or skill to complete a project. How did you approach it?",
                "category": "behavioral",
                "focus_area": "Learning agility",
                "why_asking": "Assessing your ability to adapt and learn new skills quickly."
            })
        
        # Situational question about skills gaps
        if gap_analysis.get('skills_gaps') and len(questions) < count:
            questions.append({
                "question": "If you were given a project that required skills you don't currently have, how would you approach it?",
                "category": "situational",
                "focus_area": "Problem-solving",
                "why_asking": "Understanding how you handle knowledge gaps in real-world scenarios."
            })
        
        # General technical depth question
        if len(questions) < count:
            questions.append({
                "question": "Walk me through your most technically challenging project. What made it challenging and how did you overcome those challenges?",
                "category": "technical",
                "focus_area": "Technical depth",
                "why_asking": "Assessing your technical problem-solving abilities and depth of experience."
            })
        
        # Team collaboration question
        if len(questions) < count:
            questions.append({
                "question": "Describe a situation where you had to work with a difficult team member. How did you handle it and what was the outcome?",
                "category": "behavioral",
                "focus_area": "Team collaboration",
                "why_asking": "Evaluating your interpersonal and conflict resolution skills."
            })
        
        return questions[:count]
    
    def evaluate_interview_answer(
        self,
        question: str,
        answer: str,
        job_description: str,
        resume_context: str = None
    ) -> Dict[str, Any]:
        """
        Evaluate interview answer using STAR framework
        Provides constructive feedback
        """
        
        system_prompt = """You are a professional interview coach providing feedback on interview answers.

Evaluate the answer using the STAR framework:
- Situation: Did they set up the context?
- Task: Did they explain what needed to be done?
- Action: Did they describe what THEY specifically did?
- Result: Did they share the outcome/impact?

Return ONLY a JSON object:
{
  "score": <0-100>,
  "star_analysis": {
    "situation": "<present/missing/weak>",
    "task": "<present/missing/weak>",
    "action": "<present/missing/weak>",
    "result": "<present/missing/weak>"
  },
  "strengths": ["<strength 1>", "<strength 2>"],
  "improvements": ["<improvement 1>", "<improvement 2>"],
  "suggestion": "<How to improve this answer specifically>",
  "example_reframe": "<Better way to phrase this answer>"
}"""

        user_prompt = f"""Evaluate this interview answer:

QUESTION: {question}

ANSWER: {answer}

JOB CONTEXT: {job_description[:300]}

Provide constructive feedback using STAR framework.
Return ONLY the JSON object."""

        try:
            if self.client:
                print("🤖 Evaluating answer with AI...")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                content = response.choices[0].message.content.strip()
                content = content.replace("```json", "").replace("```", "").strip()
                feedback = json.loads(content)
                print(f"✅ Evaluation complete: {feedback.get('score', 0)}/100")
                return feedback
            else:
                print("⚠️  No AI client configured, using rule-based evaluation")
        except Exception as e:
            print(f"❌ AI evaluation error: {e}")
            print("⚠️  Falling back to rule-based evaluation")
        
        # Fallback: Basic rule-based evaluation
        return self._evaluate_answer_fallback(answer)
    
    def _evaluate_answer_fallback(self, answer: str) -> Dict[str, Any]:
        """
        Basic rule-based answer evaluation when AI is unavailable
        """
        answer_lower = answer.lower()
        answer_length = len(answer.split())
        
        # Calculate score based on answer characteristics
        score = 50  # Base score
        
        star_components = {
            "situation": "missing",
            "task": "missing",
            "action": "missing",
            "result": "missing"
        }
        
        # Check for STAR elements
        situation_keywords = ["when", "while", "during", "at", "in my role"]
        task_keywords = ["needed to", "required", "had to", "was responsible", "objective"]
        action_keywords = ["i", "implemented", "developed", "created", "led", "managed"]
        result_keywords = ["resulted", "achieved", "improved", "increased", "reduced", "%"]
        
        if any(kw in answer_lower for kw in situation_keywords):
            star_components["situation"] = "present"
            score += 10
        
        if any(kw in answer_lower for kw in task_keywords):
            star_components["task"] = "present"
            score += 10
        
        if any(kw in answer_lower for kw in action_keywords):
            star_components["action"] = "present"
            score += 15
        
        if any(kw in answer_lower for kw in result_keywords):
            star_components["result"] = "present"
            score += 15
        
        # Length bonus
        if answer_length >= 50:
            score += 10
        elif answer_length < 20:
            score -= 10
        
        score = max(0, min(100, score))  # Clamp between 0-100
        
        strengths = []
        improvements = []
        
        if star_components["action"] == "present":
            strengths.append("Clearly described actions taken")
        else:
            improvements.append("Add more details about what YOU specifically did")
        
        if star_components["result"] == "present":
            strengths.append("Included outcomes or results")
        else:
            improvements.append("Include measurable results or impact")
        
        if answer_length >= 50:
            strengths.append("Provided detailed response")
        else:
            improvements.append("Expand your answer with more specific details")
        
        if not strengths:
            strengths = ["Attempted to answer the question"]
        
        if not improvements:
            improvements = ["Consider adding more context and examples"]
        
        return {
            "score": score,
            "star_analysis": star_components,
            "strengths": strengths,
            "improvements": improvements,
            "suggestion": "Try to structure your answer using the STAR framework: describe the Situation, explain the Task, detail your Actions, and share the Results.",
            "example_reframe": f"Consider rephrasing to: 'In [situation], I needed to [task]. I [specific actions], which resulted in [measurable outcome].'"
        }
    
    def generate_interview_summary(
        self,
        questions: List[str],
        answers: List[Dict[str, Any]],
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive interview performance summary
        """
        
        # Calculate average score from answers
        total_score = sum(a.get("feedback", {}).get("score", 0) for a in answers if "feedback" in a)
        avg_score = total_score / len(answers) if answers else 0
        
        # Collect all strengths and improvements
        all_strengths = []
        all_improvements = []
        
        for answer in answers:
            feedback = answer.get("feedback", {})
            all_strengths.extend(feedback.get("strengths", []))
            all_improvements.extend(feedback.get("improvements", []))
        
        # Deduplicate and limit
        unique_strengths = list(set(all_strengths))[:3]
        unique_improvements = list(set(all_improvements))[:3]
        
        return {
            "overall_score": round(avg_score),
            "performance_level": "Excellent" if avg_score >= 80 else "Good" if avg_score >= 60 else "Needs Improvement",
            "strengths": unique_strengths if unique_strengths else [
                "Engaged with all questions",
                "Demonstrated relevant experience",
                "Showed willingness to learn"
            ],
            "improvements": unique_improvements if unique_improvements else [
                "Use more specific examples with metrics",
                "Follow STAR framework more closely",
                "Connect answers more directly to job requirements"
            ],
            "recommendations": [
                "Practice answering questions using the STAR (Situation, Task, Action, Result) framework",
                "Prepare specific metrics and achievements from your experience",
                "Research the company and role more deeply to tailor your answers",
                f"Focus on improving skills in: {', '.join([k.get('keyword', '') for k in analysis.get('missing_keywords', [])[:3]])}"
            ],
            "next_steps": [
                "Review the missing keywords and work on building those skills",
                "Update your resume based on the analysis feedback",
                "Practice more mock interviews to build confidence",
                "Consider taking courses or certifications in identified gap areas"
            ]
        }
    
    def rewrite_bullet_with_star(
        self,
        original_bullet: str,
        job_description: str,
        resume_context: str = None
    ) -> Dict[str, Any]:
        """
        Rewrite a resume bullet point using STAR framework
        Emphasizes impact over tasks
        """
        
        system_prompt = """You are an expert resume writer who specializes in transforming weak bullet points into impactful STAR-format accomplishments.

Your goal is to take a task-oriented bullet and rewrite it to emphasize:
- Situation/Context (briefly)
- Task/Challenge 
- Action (specific steps YOU took)
- Result (quantifiable impact, metrics, outcomes)

Return ONLY a JSON object:
{
  "original": "<the original bullet>",
  "rewritten": "<the improved STAR-format bullet>",
  "improvements": {
    "before_issues": ["<issue 1>", "<issue 2>"],
    "after_strengths": ["<strength 1>", "<strength 2>"]
  },
  "star_breakdown": {
    "situation": "<what was the context>",
    "task": "<what needed to be done>",
    "action": "<what you specifically did>",
    "result": "<quantifiable outcome>"
  },
  "keywords_added": ["<keyword 1>", "<keyword 2>"],
  "impact_score_improvement": <0-100, how much better is this>
}

RULES:
1. Start with an action verb (Led, Developed, Implemented, Optimized, etc.)
2. Include specific metrics/numbers (%, $, time saved, users impacted)
3. Focus on RESULTS and IMPACT, not just tasks
4. Make it relevant to the target job description
5. Keep it concise (1-2 lines max)
6. Use industry-standard keywords from the JD"""

        user_prompt = f"""Rewrite this resume bullet point using STAR framework:

ORIGINAL BULLET:
{original_bullet}

TARGET JOB DESCRIPTION:
{job_description[:400]}

RESUME CONTEXT (for consistency):
{resume_context[:300] if resume_context else 'Not provided'}

Transform this into a powerful, results-oriented bullet that:
1. Shows clear impact with metrics
2. Uses relevant keywords from the JD
3. Follows STAR framework
4. Emphasizes what YOU accomplished

Return ONLY the JSON object."""

        try:
            if self.client:
                print("🤖 Rewriting bullet with AI (STAR framework)...")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                content = response.choices[0].message.content.strip()
                content = content.replace("```json", "").replace("```", "").strip()
                result = json.loads(content)
                print(f"✅ Successfully rewrote bullet")
                return result
            else:
                print("⚠️  No AI client configured, using template-based rewrite")
        except Exception as e:
            print(f"❌ AI STAR rewrite error: {e}")
            print("⚠️  Falling back to template-based rewrite")
        
        # Fallback: Template-based STAR rewrite
        return self._rewrite_bullet_fallback(original_bullet, job_description)
    
    def _rewrite_bullet_fallback(
        self,
        original_bullet: str,
        job_description: str
    ) -> Dict[str, Any]:
        """
        Template-based bullet rewrite when AI is unavailable
        """
        # Extract key action verb or add one
        action_verbs = ["Led", "Developed", "Implemented", "Managed", "Created", "Optimized", "Designed"]
        
        # Simple enhancement: add action verb if missing and suggest metrics
        rewritten = original_bullet
        if not any(verb.lower() in original_bullet.lower() for verb in action_verbs):
            rewritten = f"Developed {original_bullet.lower()}"
        
        # Add metric suggestion if missing
        if not any(char.isdigit() for char in original_bullet):
            rewritten += ", improving efficiency by 20%"
        
        return {
            "original": original_bullet,
            "rewritten": rewritten,
            "improvements": {
                "before_issues": [
                    "Lacks strong action verb at the beginning",
                    "Missing quantifiable metrics or results",
                    "Doesn't clearly show impact"
                ],
                "after_strengths": [
                    "Starts with strong action verb",
                    "Includes measurable outcome",
                    "More results-focused"
                ]
            },
            "star_breakdown": {
                "situation": "Professional work context",
                "task": "Complete project objectives",
                "action": "Applied technical skills and collaborated with team",
                "result": "Delivered successful project with measurable impact"
            },
            "keywords_added": ["efficiency", "improvement"],
            "impact_score_improvement": 35,
            "note": "⚠️ This is a template-based rewrite. For better AI-powered rewriting, configure CEREBRAS_API_KEY in your .env file."
        }
