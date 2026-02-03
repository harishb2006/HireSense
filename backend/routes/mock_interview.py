from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import uuid

from database import get_db, InterviewSession, ConversationMessage, QuestionBank, UserProfile
from services.ai_interviewer import AIInterviewer
from services.live_evaluator import LiveEvaluator
from services.interview_analyzer import InterviewAnalyzer

router = APIRouter(prefix="/api/mock-interview", tags=["Mock Interview"])

# Global cache for active interviewers (in production, use Redis)
active_interviewers: Dict[str, tuple[AIInterviewer, LiveEvaluator]] = {}


# Pydantic Models
class StartSessionRequest(BaseModel):
    user_name: str
    user_email: str
    role: str  # e.g., "Node.js Developer"
    seniority_level: str  # e.g., "Senior", "Mid", "Junior"


class StartSessionResponse(BaseModel):
    session_id: str
    first_question: str
    message_number: int


class SendAnswerRequest(BaseModel):
    session_id: str
    answer: str


class SendAnswerResponse(BaseModel):
    next_question: str
    depth_score: Optional[float]
    clarity_score: Optional[float]
    confidence_score: Optional[float]
    overall_score: Optional[float]
    message_number: int
    is_follow_up: bool
    current_topic: Optional[str]
    session_status: str  # active or completed


class GetSessionResponse(BaseModel):
    session_id: str
    role: str
    seniority_level: str
    status: str
    started_at: datetime
    total_messages: int
    current_score: float


class ConversationHistory(BaseModel):
    role: str
    message: str
    timestamp: datetime
    message_number: int
    scores: Optional[dict]


@router.post("/start", response_model=StartSessionResponse)
async def start_interview_session(
    request: StartSessionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Start a new mock interview session with AI-driven adaptive questioning.
    Creates user if doesn't exist, initializes AI interviewer, and asks dynamic first question.
    """
    # Create or get user
    result = await db.execute(
        select(UserProfile).where(UserProfile.email == request.user_email)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        user = UserProfile(
            name=request.user_name,
            email=request.user_email
        )
        db.add(user)
        await db.flush()
    
    # Get available topics for this role from question bank
    topics_result = await db.execute(
        select(QuestionBank.category)
        .where(
            QuestionBank.role == request.role,
            QuestionBank.seniority_level == request.seniority_level
        )
        .distinct()
    )
    available_topics = [row[0] for row in topics_result.fetchall()]
    
    if not available_topics:
        # Fallback to generic topics
        available_topics = ["Core Concepts", "Best Practices", "Problem Solving"]
    
    # Initialize AI Interviewer and Evaluator
    ai_interviewer = AIInterviewer(request.role, request.seniority_level)
    live_evaluator = LiveEvaluator()
    
    # Generate opening question
    opening = ai_interviewer.generate_opening_question(available_topics)
    
    # Create new interview session
    session = InterviewSession(
        user_id=user.id,
        role=request.role,
        seniority_level=request.seniority_level,
        status="active",
        current_topic=opening.get("topic"),
        ai_context=ai_interviewer.get_state()
    )
    db.add(session)
    await db.flush()
    
    # Cache the interviewer and evaluator
    active_interviewers[str(session.id)] = (ai_interviewer, live_evaluator)
    
    # Save first question as assistant message
    first_message = ConversationMessage(
        session_id=session.id,
        role="assistant",
        message=opening["question"],
        message_number=1,
        topic=opening.get("topic"),
        model_answer=opening.get("ideal_answer")
    )
    db.add(first_message)
    await db.commit()
    
    return StartSessionResponse(
        session_id=str(session.id),
        first_question=opening["question"],
        message_number=1
    )


@router.post("/answer", response_model=SendAnswerResponse)
async def submit_answer(
    request: SendAnswerRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit user's answer and get adaptive next question.
    Uses AI to analyze depth, detect gaps, and generate follow-up questions.
    """
    session_id = uuid.UUID(request.session_id)
    
    # Verify session exists and is active
    result = await db.execute(
        select(InterviewSession).where(InterviewSession.id == session_id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.status != "active":
        raise HTTPException(status_code=400, detail="Session is not active")
    
    # Get or restore AI interviewer and evaluator
    session_id_str = str(session_id)
    if session_id_str in active_interviewers:
        ai_interviewer, live_evaluator = active_interviewers[session_id_str]
    else:
        # Restore from database
        ai_interviewer = AIInterviewer(session.role, session.seniority_level)
        ai_interviewer.restore_state({
            "knowledge_map": session.knowledge_map or {},
            "topics_covered": session.topics_covered or [],
            "current_topic": session.current_topic,
            "follow_up_queue": session.follow_up_queue or []
        })
        live_evaluator = LiveEvaluator()
        active_interviewers[session_id_str] = (ai_interviewer, live_evaluator)
    
    # Get last assistant question
    last_q_result = await db.execute(
        select(ConversationMessage)
        .where(
            ConversationMessage.session_id == session_id,
            ConversationMessage.role == "assistant"
        )
        .order_by(desc(ConversationMessage.message_number))
        .limit(1)
    )
    last_question_msg = last_q_result.scalar_one_or_none()
    last_question = last_question_msg.message if last_question_msg else ""
    ideal_answer = last_question_msg.model_answer if last_question_msg else None
    
    # Get message count for numbering
    count_result = await db.execute(
        select(func.count(ConversationMessage.id))
        .where(ConversationMessage.session_id == session_id)
    )
    message_count = count_result.scalar() or 0
    
    # Analyze answer using AI
    analysis = ai_interviewer.analyze_answer_depth(
        last_question,
        request.answer,
        ideal_answer or ""
    )
    
    # Live evaluation
    live_scores = live_evaluator.evaluate_response(
        last_question,
        request.answer,
        ideal_answer
    )
    
    # Extract keywords
    keywords = ai_interviewer.extract_keywords(request.answer)
    
    # Save user's answer
    user_message = ConversationMessage(
        session_id=session_id,
        role="user",
        message=request.answer,
        message_number=message_count + 1,
        depth_score=live_scores["technical_depth_score"],
        clarity_score=live_scores["clarity_score"],
        confidence_score=live_scores["confidence_score"],
        topic=session.current_topic,
        keywords_detected=keywords
    )
    db.add(user_message)
    
    # Calculate interview duration
    duration = (datetime.utcnow() - session.started_at).total_seconds() / 60
    questions_asked = (message_count + 1) // 2  # Every 2 messages = 1 Q&A pair
    
    # Check if interview should end
    should_end, end_reason = ai_interviewer.should_end_interview(
        duration, questions_asked
    )
    
    if should_end:
        # Generate closing message
        session.status = "completed"
        session.ended_at = datetime.utcnow()
        session.duration_minutes = int(duration)
        
        # Update final scores
        cumulative = live_evaluator.get_cumulative_scores()
        session.technical_depth_score = cumulative["technical_depth"]
        session.clarity_score = cumulative["clarity"]
        session.confidence_score = cumulative["confidence"]
        session.total_score = live_evaluator.get_overall_score()
        
        # Save state
        session.knowledge_map = ai_interviewer.get_knowledge_map()
        session.topics_covered = ai_interviewer.topics_covered
        session.ai_context = ai_interviewer.get_state()
        
        closing_msg = f"Thank you for completing the interview! Your overall score is {session.total_score}/10. You'll receive a detailed analysis shortly."
        
        assistant_message = ConversationMessage(
            session_id=session_id,
            role="assistant",
            message=closing_msg,
            message_number=message_count + 2,
            is_follow_up="false"
        )
        db.add(assistant_message)
        await db.commit()
        
        # Clean up cache
        if session_id_str in active_interviewers:
            del active_interviewers[session_id_str]
        
        return SendAnswerResponse(
            next_question=closing_msg,
            depth_score=live_scores["technical_depth_score"],
            clarity_score=live_scores["clarity_score"],
            confidence_score=live_scores["confidence_score"],
            overall_score=live_scores["overall_score"],
            message_number=message_count + 2,
            is_follow_up=False,
            current_topic=session.current_topic,
            session_status="completed"
        )
    
    # Determine next question strategy
    needs_follow_up = analysis.get("needs_follow_up", False)
    is_follow_up = False
    
    if needs_follow_up or analysis["technical_depth_score"] < 7:
        # Generate drill-down follow-up question
        next_q = ai_interviewer.generate_follow_up_question(
            last_question,
            request.answer,
            analysis
        )
        is_follow_up = True
    else:
        # Move to new topic
        available_topics = ["Performance", "Security", "Scalability", "Design Patterns"]
        uncovered = [t for t in available_topics if t not in ai_interviewer.topics_covered]
        
        if uncovered:
            new_topic = uncovered[0]
            next_q = ai_interviewer.generate_transition_question(new_topic)
        else:
            # Generate advanced question on current topic
            next_q = ai_interviewer.generate_follow_up_question(
                last_question,
                request.answer,
                analysis
            )
            is_follow_up = True
    
    # Save assistant's next question
    assistant_message = ConversationMessage(
        session_id=session_id,
        role="assistant",
        message=next_q["question"],
        message_number=message_count + 2,
        is_follow_up="true" if is_follow_up else "false",
        topic=ai_interviewer.current_topic,
        model_answer=next_q.get("ideal_answer")
    )
    db.add(assistant_message)
    
    # Update session state
    session.current_topic = ai_interviewer.current_topic
    session.topics_covered = ai_interviewer.topics_covered
    session.knowledge_map = ai_interviewer.get_knowledge_map()
    session.ai_context = ai_interviewer.get_state()
    
    # Update running scores
    cumulative = live_evaluator.get_cumulative_scores()
    session.technical_depth_score = cumulative["technical_depth"]
    session.clarity_score = cumulative["clarity"]
    session.confidence_score = cumulative["confidence"]
    session.total_score = live_evaluator.get_overall_score()
    
    await db.commit()
    
    return SendAnswerResponse(
        next_question=next_q["question"],
        depth_score=live_scores["technical_depth_score"],
        clarity_score=live_scores["clarity_score"],
        confidence_score=live_scores["confidence_score"],
        overall_score=live_scores["overall_score"],
        message_number=message_count + 2,
        is_follow_up=is_follow_up,
        current_topic=ai_interviewer.current_topic,
        session_status="active"
    )


@router.get("/session/{session_id}", response_model=GetSessionResponse)
async def get_session_info(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get current session information."""
    session_uuid = uuid.UUID(session_id)
    
    result = await db.execute(
        select(InterviewSession).where(InterviewSession.id == session_uuid)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Count messages
    message_result = await db.execute(
        select(ConversationMessage)
        .where(ConversationMessage.session_id == session_uuid)
    )
    messages = message_result.scalars().all()
    
    return GetSessionResponse(
        session_id=str(session.id),
        role=session.role,
        seniority_level=session.seniority_level,
        status=session.status,
        started_at=session.started_at,
        total_messages=len(messages),
        current_score=float(session.total_score or 0)
    )


@router.get("/session/{session_id}/history", response_model=List[ConversationHistory])
async def get_conversation_history(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get full conversation history for a session."""
    session_uuid = uuid.UUID(session_id)
    
    result = await db.execute(
        select(ConversationMessage)
        .where(ConversationMessage.session_id == session_uuid)
        .order_by(ConversationMessage.message_number)
    )
    messages = result.scalars().all()
    
    history = []
    for msg in messages:
        scores = None
        if msg.role == "user" and msg.depth_score:
            scores = {
                "depth": float(msg.depth_score),
                "clarity": float(msg.clarity_score),
                "confidence": float(msg.confidence_score)
            }
        
        history.append(ConversationHistory(
            role=msg.role,
            message=msg.message,
            timestamp=msg.timestamp,
            message_number=msg.message_number,
            scores=scores
        ))
    
    return history


@router.get("/session/{session_id}/knowledge-map")
async def get_knowledge_map(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get the AI-generated knowledge map showing user's strengths and weaknesses.
    This is the "Weakness Detection" feature.
    """
    session_uuid = uuid.UUID(session_id)
    
    result = await db.execute(
        select(InterviewSession).where(InterviewSession.id == session_uuid)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": str(session.id),
        "role": session.role,
        "seniority_level": session.seniority_level,
        "knowledge_map": session.knowledge_map or {},
        "topics_covered": session.topics_covered or [],
        "overall_assessment": {
            "technical_depth": float(session.technical_depth_score or 0),
            "clarity": float(session.clarity_score or 0),
            "confidence": float(session.confidence_score or 0),
            "total_score": float(session.total_score or 0)
        }
    }


@router.post("/session/{session_id}/end")
async def end_session(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """End the interview session and finalize scores."""
    session_uuid = uuid.UUID(session_id)
    
    # Check if interviewer is in cache
    if str(session_uuid) in active_interviewers:
        ai_interviewer, live_evaluator = active_interviewers[str(session_uuid)]
        
        result = await db.execute(
            select(InterviewSession).where(InterviewSession.id == session_uuid)
        )
        session = result.scalar_one_or_none()
        
        if session:
            # Calculate duration
            duration = (datetime.utcnow() - session.started_at).total_seconds() / 60
            
            # Update session with final data
            session.status = "completed"
            session.ended_at = datetime.utcnow()
            session.duration_minutes = int(duration)
            session.knowledge_map = ai_interviewer.get_knowledge_map()
            session.topics_covered = ai_interviewer.topics_covered
            
            # Get final scores
            cumulative = live_evaluator.get_cumulative_scores()
            session.technical_depth_score = cumulative["technical_depth"]
            session.clarity_score = cumulative["clarity"]
            session.confidence_score = cumulative["confidence"]
            session.total_score = live_evaluator.get_overall_score()
            
            await db.commit()
            
            # Clean up cache
            del active_interviewers[str(session_uuid)]
            
            return {
                "message": "Session ended successfully",
                "session_id": str(session.id),
                "duration_minutes": session.duration_minutes,
                "final_score": float(session.total_score),
                "knowledge_map": session.knowledge_map
            }
    
    result = await db.execute(
        select(InterviewSession).where(InterviewSession.id == session_uuid)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Calculate duration
    duration = (datetime.utcnow() - session.started_at).total_seconds() / 60
    
    # Update session
    session.status = "completed"
    session.ended_at = datetime.utcnow()
    session.duration_minutes = int(duration)
    
    await db.commit()
    
    return {
        "message": "Session ended successfully",
        "session_id": str(session.id),
        "duration_minutes": session.duration_minutes,
        "final_score": float(session.total_score)
    }


@router.get("/session/{session_id}/report")
async def get_interview_report(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate comprehensive post-interview debrief report.
    Includes transcript vs model answers, knowledge map, and recommendations.
    """
    session_uuid = uuid.UUID(session_id)
    
    # Get session
    result = await db.execute(
        select(InterviewSession).where(InterviewSession.id == session_uuid)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get conversation history
    history_result = await db.execute(
        select(ConversationMessage)
        .where(ConversationMessage.session_id == session_uuid)
        .order_by(ConversationMessage.message_number)
    )
    messages = history_result.scalars().all()
    
    # Convert to dict format
    conversation_history = [
        {
            "role": msg.role,
            "message": msg.message,
            "depth_score": float(msg.depth_score) if msg.depth_score else None,
            "clarity_score": float(msg.clarity_score) if msg.clarity_score else None,
            "confidence_score": float(msg.confidence_score) if msg.confidence_score else None,
            "topic": msg.topic,
            "model_answer": msg.model_answer,
            "is_follow_up": msg.is_follow_up,
            "keywords_detected": msg.keywords_detected,
            "timestamp": msg.timestamp
        }
        for msg in messages
    ]
    
    # Prepare session data
    session_data = {
        "session_id": str(session.id),
        "role": session.role,
        "seniority_level": session.seniority_level,
        "duration_minutes": session.duration_minutes,
        "total_score": float(session.total_score or 0),
        "technical_depth_score": float(session.technical_depth_score or 0),
        "clarity_score": float(session.clarity_score or 0),
        "confidence_score": float(session.confidence_score or 0),
        "knowledge_map": session.knowledge_map or {},
        "topics_covered": session.topics_covered or []
    }
    
    # Generate report
    analyzer = InterviewAnalyzer()
    report = analyzer.generate_debrief_report(session_data, conversation_history)
    
    return report


@router.get("/session/{session_id}/report/html")
async def get_interview_report_html(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get HTML version of interview report for better visualization.
    """
    from fastapi.responses import HTMLResponse
    
    session_uuid = uuid.UUID(session_id)
    
    # Get session and messages (same as above)
    result = await db.execute(
        select(InterviewSession).where(InterviewSession.id == session_uuid)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    history_result = await db.execute(
        select(ConversationMessage)
        .where(ConversationMessage.session_id == session_uuid)
        .order_by(ConversationMessage.message_number)
    )
    messages = history_result.scalars().all()
    
    conversation_history = [
        {
            "role": msg.role,
            "message": msg.message,
            "depth_score": float(msg.depth_score) if msg.depth_score else None,
            "clarity_score": float(msg.clarity_score) if msg.clarity_score else None,
            "confidence_score": float(msg.confidence_score) if msg.confidence_score else None,
            "topic": msg.topic,
            "model_answer": msg.model_answer,
            "is_follow_up": msg.is_follow_up,
            "keywords_detected": msg.keywords_detected,
            "timestamp": msg.timestamp
        }
        for msg in messages
    ]
    
    session_data = {
        "session_id": str(session.id),
        "role": session.role,
        "seniority_level": session.seniority_level,
        "duration_minutes": session.duration_minutes,
        "total_score": float(session.total_score or 0),
        "technical_depth_score": float(session.technical_depth_score or 0),
        "clarity_score": float(session.clarity_score or 0),
        "confidence_score": float(session.confidence_score or 0),
        "knowledge_map": session.knowledge_map or {},
        "topics_covered": session.topics_covered or []
    }
    
    analyzer = InterviewAnalyzer()
    report = analyzer.generate_debrief_report(session_data, conversation_history)
    html_content = analyzer.generate_html_report(report)
    
    return HTMLResponse(content=html_content)
