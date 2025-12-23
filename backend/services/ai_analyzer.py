import json
import os
from typing import Dict, Any

class AIAnalyzer:
    """
    AI-powered resume analysis service
    Returns structured JSON output for resume analysis
    """
    
    def __init__(self):
        # In production, use environment variables for API keys
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        
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
        
        prompt = self._build_analysis_prompt(resume_text, job_description)
        
        # TODO: Integrate with actual LLM (OpenAI, Anthropic, etc.)
        # For now, returning mock structured data
        # When integrating real LLM, ensure prompt enforces JSON-only output
        
        analysis = self._call_llm(prompt)
        
        return analysis
    
    def _build_analysis_prompt(self, resume_text: str, job_description: str) -> str:
        """
        Build the prompt for LLM analysis
        CRITICAL: Instructs LLM to return ONLY valid JSON
        """
        
        prompt = f"""You are an expert ATS (Applicant Tracking System) and resume analyzer.

Analyze the following resume against the job description and return ONLY a valid JSON object with no additional text.

Job Description:
{job_description}

Resume:
{resume_text}

Return ONLY valid JSON in this exact format (no markdown, no explanation, no additional text):
{{
  "match_score": <number between 0-100>,
  "missing_keywords": [<array of important missing keywords from JD>],
  "section_feedback": {{
    "Summary": "<specific feedback on summary/objective section>",
    "Experience": "<specific feedback on experience section>",
    "Skills": "<specific feedback on skills section>"
  }}
}}

Rules:
1. match_score: Calculate based on keyword matches, experience alignment, and skill coverage (0-100)
2. missing_keywords: List 5-10 critical keywords/technologies from JD that are missing in resume
3. section_feedback: Provide actionable, specific feedback for each section
4. Return ONLY the JSON object, no other text

JSON OUTPUT:"""

        return prompt
    
    def _call_llm(self, prompt: str) -> Dict[str, Any]:
        """
        Call LLM API and parse JSON response
        
        In production, integrate with:
        - OpenAI GPT-4
        - Anthropic Claude
        - Google Gemini
        - Local LLM (Llama, Mistral)
        """
        
        # TODO: Replace with actual LLM API call
        # Example for OpenAI:
        # import openai
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=0.3
        # )
        # return json.loads(response.choices[0].message.content)
        
        # Mock response for development/testing
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
