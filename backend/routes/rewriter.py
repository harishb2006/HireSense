from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
from services.pdf_generator import PDFScorecard
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
import io

router = APIRouter(prefix="/api/rewriter", tags=["STAR Rewriter"])

class StarRewriteRequest(BaseModel):
    original_bullet: str
    job_description: str
    resume_context: Optional[str] = None

class ScorecardRequest(BaseModel):
    analysis: Dict[str, Any]
    interview_summary: Optional[Dict[str, Any]] = None
    candidate_name: str = "Candidate"

@router.post("/star-rewrite")
async def rewrite_bullet_star(payload: StarRewriteRequest) -> Dict[str, Any]:
    """
    Rewrite a resume bullet point using STAR framework
    Emphasizes impact over tasks
    """
    
    if not payload.original_bullet.strip():
        raise HTTPException(status_code=400, detail="Original bullet cannot be empty")
    
    if not payload.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")
    
    try:
        # Initialize Cerebras AI via LangChain
        llm = ChatOpenAI(
            model="llama3.3-70b",
            api_key=os.getenv("CEREBRAS_API_KEY"),
            base_url="https://api.cerebras.ai/v1",
            temperature=0.7
        )
        
        # Construct the prompt
        system_prompt = """You are an expert resume writer specializing in the STAR (Situation, Task, Action, Result) framework.
Your job is to transform weak, task-focused bullet points into powerful, impact-driven accomplishments.

STAR Framework:
- Situation: Brief context (when needed)
- Task: Your responsibility
- Action: What YOU did specifically
- Result: Quantifiable impact/outcome

Guidelines:
1. Start with strong action verbs
2. Include metrics and numbers whenever possible
3. Focus on achievements, not duties
4. Keep it concise (1-2 lines max)
5. Tailor to the target job description
6. Remove vague language like "helped with" or "responsible for"

Return a JSON object with these fields:
{
    "original": "the original bullet",
    "rewritten": "the STAR-formatted bullet",
    "improvements": ["list of key improvements made"],
    "impact_score": 1-10 (how much stronger is the new version)
}"""

        context_note = f"\n\nAdditional resume context:\n{payload.resume_context}" if payload.resume_context else ""
        
        user_prompt = f"""Job Description:
{payload.job_description}

Original Bullet Point:
{payload.original_bullet}{context_note}

Rewrite this bullet point using the STAR framework to maximize impact and alignment with the job description."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        
        # Parse the response
        import json
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            # If AI doesn't return valid JSON, create a structured response
            result = {
                "original": payload.original_bullet,
                "rewritten": response.content,
                "improvements": ["AI-enhanced with STAR framework"],
                "impact_score": 7
            }
        
        return result
    
    except Exception as e:
        print(f"❌ STAR rewrite error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"STAR rewrite failed: {str(e)}"
        )

@router.post("/generate-scorecard")
async def generate_pdf_scorecard(payload: ScorecardRequest):
    """
    Generate downloadable PDF scorecard with analysis and interview results
    """
    
    try:
        generator = PDFScorecard()
        pdf_bytes = generator.generate_full_scorecard(
            analysis=payload.analysis,
            interview_summary=payload.interview_summary,
            candidate_name=payload.candidate_name
        )
        
        # Return as downloadable PDF
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=HireSense_Scorecard_{payload.candidate_name.replace(' ', '_')}.pdf"
            }
        )
    
    except Exception as e:
        print(f"❌ PDF generation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"PDF generation failed: {str(e)}"
        )
