from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_analyzer import AIAnalyzer

router = APIRouter(prefix="/api", tags=["Analysis"])

class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str

class SectionFeedback(BaseModel):
    Summary: str
    Experience: str
    Skills: str

class AnalysisResponse(BaseModel):
    match_score: int
    missing_keywords: list[str]
    section_feedback: SectionFeedback

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(payload: AnalyzeRequest):
    """
    AI-powered resume analysis endpoint
    
    Returns structured JSON with:
    - match_score: 0-100 score indicating resume-JD alignment
    - missing_keywords: Array of important missing keywords
    - section_feedback: Detailed feedback for each resume section
    """
    
    if not payload.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text cannot be empty")
    
    if not payload.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")
    
    try:
        analyzer = AIAnalyzer()
        analysis = analyzer.analyze_resume(
            resume_text=payload.resume_text,
            job_description=payload.job_description
        )
        
        # Validate the output structure
        if not analyzer.validate_analysis_output(analysis):
            raise HTTPException(
                status_code=500,
                detail="AI analysis returned invalid structure"
            )
        
        return analysis
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
