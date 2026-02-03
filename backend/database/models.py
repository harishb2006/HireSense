from sqlalchemy import Column, String, Integer, Numeric, DateTime, Text, ARRAY, ForeignKey, BigInteger, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()


class UserProfile(Base):
    __tablename__ = 'user_profiles'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    total_interviews = Column(Integer, default=0)
    avg_score = Column(Numeric(5, 2), default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sessions = relationship("InterviewSession", back_populates="user", cascade="all, delete-orphan")


class InterviewSession(Base):
    __tablename__ = 'interview_sessions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user_profiles.id', ondelete='CASCADE'))
    role = Column(String(100), nullable=False)
    seniority_level = Column(String(50), nullable=False)
    status = Column(String(50), default='active')
    total_score = Column(Numeric(5, 2), default=0.0)
    technical_depth_score = Column(Numeric(5, 2), default=0.0)
    clarity_score = Column(Numeric(5, 2), default=0.0)
    confidence_score = Column(Numeric(5, 2), default=0.0)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, default=0)
    
    # Conversation state for AI memory
    ai_context = Column(JSONB, default={})  # Stores AI's understanding of user's strengths/weaknesses
    follow_up_queue = Column(JSONB, default=[])  # Queue of follow-up questions to drill down
    knowledge_map = Column(JSONB, default={})  # Tracks user's knowledge across topics
    current_topic = Column(String(100), nullable=True)  # Current topic being discussed
    topics_covered = Column(ARRAY(Text), default=[])  # Topics already covered
    
    # Relationships
    user = relationship("UserProfile", back_populates="sessions")
    messages = relationship("ConversationMessage", back_populates="session", cascade="all, delete-orphan")


class ConversationMessage(Base):
    __tablename__ = 'conversation_messages'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey('interview_sessions.id', ondelete='CASCADE'))
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    message = Column(Text, nullable=False)
    depth_score = Column(Numeric(5, 2), nullable=True)
    clarity_score = Column(Numeric(5, 2), nullable=True)
    confidence_score = Column(Numeric(5, 2), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    message_number = Column(Integer, nullable=False)
    
    # AI Analysis metadata
    is_follow_up = Column(String(10), default='false')  # 'true' if this was a drill-down question
    topic = Column(String(100), nullable=True)  # Topic this message relates to
    keywords_detected = Column(ARRAY(Text), default=[])  # Key technical terms mentioned
    model_answer = Column(Text, nullable=True)  # Ideal answer for comparison (for AI questions)
    
    # Relationships
    session = relationship("InterviewSession", back_populates="messages")


class QuestionBank(Base):
    __tablename__ = 'question_bank'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    seniority_level = Column(String(50), nullable=False)
    question_text = Column(Text, nullable=False)
    ideal_answer = Column(Text, nullable=False)
    follow_up_hints = Column(JSONB, default=[])
    tags = Column(ARRAY(Text), default=[])
    difficulty = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.utcnow)
