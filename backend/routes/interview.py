from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from services.ai_analyzer import AIAnalyzer
from services.pdf_parcer import extract_text_from_pdf
import json

router = APIRouter(prefix="/api/interview", tags=["Mock Interview"])

class InterviewQuestionRequest(BaseModel):
    resume_text: str
    job_description: str
    analysis: Dict[str, Any]  # Previous analysis results
    question_count: int = 5

class AnswerFeedbackRequest(BaseModel):
    question: str
    answer: str
    job_description: str
    resume_context: Optional[str] = None

class InterviewSession(BaseModel):
    session_id: str
    resume_text: str
    job_description: str
    analysis: Dict[str, Any]
    questions: List[str] = []
    answers: List[Dict[str, Any]] = []

@router.post("/generate-questions")
async def generate_interview_questions(payload: InterviewQuestionRequest) -> Dict[str, Any]:
    """
    Generate targeted interview questions based on resume analysis
    Focuses on weak areas and missing skills
    """
    try:
        analyzer = AIAnalyzer()
        questions = analyzer.generate_interview_questions(
            resume_text=payload.resume_text,
            job_description=payload.job_description,
            analysis=payload.analysis,
            count=payload.question_count
        )
        
        return {
            "questions": questions,
            "total": len(questions),
            "focus_areas": payload.analysis.get("missing_keywords", [])[:5]
        }
    
    except Exception as e:
        print(f"❌ Question generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate questions: {str(e)}")

@router.post("/evaluate-answer")
async def evaluate_answer(payload: AnswerFeedbackRequest) -> Dict[str, Any]:
    """
    Evaluate user's answer using STAR framework
    Provides constructive feedback
    """
    try:
        analyzer = AIAnalyzer()
        feedback = analyzer.evaluate_interview_answer(
            question=payload.question,
            answer=payload.answer,
            job_description=payload.job_description,
            resume_context=payload.resume_context
        )
        
        return feedback
    
    except Exception as e:
        print(f"❌ Answer evaluation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to evaluate answer: {str(e)}")

@router.post("/complete-interview")
async def complete_interview(session: InterviewSession) -> Dict[str, Any]:
    """
    Generate comprehensive interview feedback
    """
    try:
        analyzer = AIAnalyzer()
        feedback = analyzer.generate_interview_summary(
            questions=session.questions,
            answers=session.answers,
            analysis=session.analysis
        )
        
        return feedback
    
    except Exception as e:
        print(f"❌ Interview completion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")

@router.post("/start-interview")
async def start_interview(
    file: UploadFile = File(...),
    job_description: str = Form(...)
) -> Dict[str, Any]:
    """
    Complete workflow: Upload resume, analyze with AI, and generate interview questions
    
    Returns:
    - resume_text: Extracted text from PDF
    - filename: Original filename
    - analysis: AI-powered resume analysis (match score, gaps, feedback)
    - interview: Generated questions based on weak areas
    """
    try:
        # Step 1: Extract text from PDF
        pdf_content = await file.read()
        resume_text = extract_text_from_pdf(pdf_content)
        
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Step 2: AI Analysis
        analyzer = AIAnalyzer()
        analysis = analyzer.analyze_resume(
            resume_text=resume_text,
            job_description=job_description
        )
        
        # Step 3: Generate interview questions based on analysis
        questions = analyzer.generate_interview_questions(
            resume_text=resume_text,
            job_description=job_description,
            analysis=analysis,
            count=5
        )
        
        return {
            "resume_text": resume_text,
            "filename": file.filename,
            "analysis": analysis,
            "interview": {
                "questions": questions,
                "focus_areas": analysis.get("missing_keywords", [])[:5]
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Start interview error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to start interview: {str(e)}")
