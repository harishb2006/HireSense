import json
import os
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIAnalyzer:
    """
    AI-powered resume analysis service using OpenAI
    Returns structured JSON output for resume analysis
    """
    
    def __init__(self):
        # Load API key from environment variables
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        # Initialize OpenAI client if API key exists
        self.client = None
        if self.api_key and self.api_key != "your-api-key-here":
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize OpenAI client: {e}")
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
        
        system_prompt = """You are an expert ATS (Applicant Tracking System) and resume analyzer with years of experience in recruitment.

Your task is to analyze resumes against job descriptions and provide detailed, actionable feedback.

You MUST return ONLY a valid JSON object with no additional text, explanations, or markdown formatting.

The JSON must follow this exact structure:
{
  "match_score": <number between 0-100>,
  "missing_keywords": [<array of 5-10 important missing keywords from job description>],
  "section_feedback": {
    "Summary": "<specific feedback on summary/objective>",
    "Experience": "<specific feedback on work experience>",
    "Skills": "<specific feedback on skills section>"
  }
}

Rules:
1. match_score: Calculate based on keyword matches, experience alignment, and skill coverage
2. missing_keywords: List critical keywords/technologies from JD that are absent in resume
3. section_feedback: Provide specific, actionable feedback for each section
4. Be constructive and professional in your feedback"""

        user_prompt = f"""Analyze this resume against the job description:

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Return ONLY the JSON object, no other text."""

        return system_prompt, user_prompt
    
    def _call_llm(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Call OpenAI API and parse JSON response
        Falls back to mock data if API key not configured
        """
        
        # If OpenAI client is configured, use it
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
                
                # Parse the JSON response
                content = response.choices[0].message.content
                analysis = json.loads(content)
                
                return analysis
                
            except json.JSONDecodeError as e:
                print(f"Error: Failed to parse JSON from OpenAI response: {e}")
                return self._get_mock_response()
            except Exception as e:
                print(f"Error calling OpenAI API: {e}")
                return self._get_mock_response()
        
        # Fall back to mock response if no API key
        print("Warning: Using mock response. Set OPENAI_API_KEY in .env file to use real AI analysis")
        return self._get_mock_response()
    
    def _get_mock_response(self) -> Dict[str, Any]:
        """
        Return mock response for development/testing
        """
        mock_response = {
            "match_score": 72,
            "missing_keywords": [
                "Docker",
                "Kubernetes",
                "System Design",
                "Microservices",
                "CI/CD",
                "AWS Lambda"
            ],
            "section_feedback": {
                "Summary": "Too generic and lacks specific alignment with the role. Consider highlighting relevant technical skills and years of experience mentioned in the JD.",
                "Experience": "Strong demonstration of impact and responsibilities, but missing quantifiable metrics. Add specific numbers for performance improvements, team size, or project scale.",
                "Skills": "Good foundation but needs cloud technologies like AWS, Docker, and container orchestration tools mentioned in the job requirements."
            }
        }
        
        return mock_response
    
    def validate_analysis_output(self, analysis: Dict[str, Any]) -> bool:
        """
        Validate that the analysis output matches expected schema
        """
        required_fields = ["match_score", "missing_keywords", "section_feedback"]
        
        if not all(field in analysis for field in required_fields):
            return False
        
        if not isinstance(analysis["match_score"], (int, float)):
            return False
        
        if not isinstance(analysis["missing_keywords"], list):
            return False
        
        if not isinstance(analysis["section_feedback"], dict):
            return False
        
        return True
