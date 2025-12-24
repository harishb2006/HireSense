import json
import os
from typing import Dict, Any
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
