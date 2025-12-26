from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
from services.ai_analyzer import AIAnalyzer
from services.pdf_generator import PDFScorecard
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
        analyzer = AIAnalyzer()
        result = analyzer.rewrite_bullet_with_star(
            original_bullet=payload.original_bullet,
            job_description=payload.job_description,
            resume_context=payload.resume_context
        )
        
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
