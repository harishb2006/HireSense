"""
AI Interviewer Service - Dynamic State-Aware Interview System
Handles adaptive questioning, depth detection, and multi-turn conversations
"""

import os
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage


class AIInterviewer:
    """
    State-aware AI interviewer that maintains conversation context,
    detects answer depth, and generates adaptive follow-up questions.
    """
    
    def __init__(self, role: str, seniority_level: str):
        self.role = role
        self.seniority_level = seniority_level
        
        # Initialize Cerebras LLM via OpenAI-compatible API
        self.llm = ChatOpenAI(
            base_url="https://api.cerebras.ai/v1",
            api_key=os.environ.get("CEREBRAS_API_KEY"),
            model=os.environ.get("CEREBRAS_MODEL", "llama-3.3-70b"),
            temperature=0.7,
            max_tokens=2000
        )
        
        # Conversation state
        self.conversation_history = []
        self.knowledge_map = {}
        self.topics_covered = []
        self.current_topic = None
        self.follow_up_queue = []
        
    def generate_opening_question(self, topics: List[str]) -> Dict:
        """
        Generate the first question based on role and seniority level.
        """
        prompt = f"""You are an expert technical interviewer for a {self.seniority_level} {self.role} position.

Generate a compelling opening question that:
1. Tests fundamental understanding of a core concept
2. Is appropriate for {self.seniority_level} level
3. Allows for both breadth and depth in the answer
4. Focuses on one of these topics: {', '.join(topics)}

Return your response in JSON format:
{{
    "question": "The interview question",
    "topic": "The main topic (e.g., Event Loop, React Hooks, etc.)",
    "ideal_answer": "A comprehensive model answer",
    "key_concepts": ["concept1", "concept2", "concept3"],
    "follow_up_hints": ["potential follow-up 1", "potential follow-up 2"]
}}"""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        result = self._parse_json_response(response.content)
        
        self.current_topic = result.get("topic")
        self.follow_up_queue = result.get("follow_up_hints", [])
        
        return result
    
    def analyze_answer_depth(self, question: str, user_answer: str, 
                            ideal_answer: str) -> Dict:
        """
        Analyze the depth and quality of user's answer.
        Returns scores and identifies gaps in knowledge.
        """
        prompt = f"""You are an expert technical interviewer evaluating a candidate's answer.

QUESTION: {question}

USER'S ANSWER: {user_answer}

IDEAL ANSWER: {ideal_answer}

Analyze the user's answer and provide:
1. Technical Depth Score (0-10): How deep is their technical understanding?
2. Clarity Score (0-10): How well did they explain their answer?
3. Confidence Indicators: Does the answer show confidence or uncertainty?
4. Missing Key Concepts: What important concepts did they miss?
5. Strong Points: What did they explain well?

Return your analysis in JSON format:
{{
    "technical_depth_score": 0-10,
    "clarity_score": 0-10,
    "confidence_score": 0-10,
    "missing_concepts": ["concept1", "concept2"],
    "strong_points": ["point1", "point2"],
    "needs_follow_up": true/false,
    "reasoning": "Brief explanation of scores"
}}"""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        analysis = self._parse_json_response(response.content)
        
        # Update knowledge map
        topic = self.current_topic
        if topic not in self.knowledge_map:
            self.knowledge_map[topic] = {
                "scores": [],
                "strong_areas": [],
                "weak_areas": []
            }
        
        self.knowledge_map[topic]["scores"].append(analysis["technical_depth_score"])
        self.knowledge_map[topic]["strong_areas"].extend(analysis.get("strong_points", []))
        self.knowledge_map[topic]["weak_areas"].extend(analysis.get("missing_concepts", []))
        
        return analysis
    
    def generate_follow_up_question(self, previous_q: str, user_answer: str, 
                                   analysis: Dict) -> Dict:
        """
        Generate adaptive follow-up question based on answer analysis.
        Drills down into areas where the candidate showed weakness.
        """
        if analysis["technical_depth_score"] >= 8:
            # Answer was strong, move to a different aspect or harder question
            strategy = "advance to more challenging aspect"
        elif analysis["technical_depth_score"] >= 5:
            # Moderate answer, dig deeper into the same topic
            strategy = "dig deeper into the current topic"
        else:
            # Weak answer, probe fundamentals
            strategy = "test fundamental understanding"
        
        missing_concepts = analysis.get("missing_concepts", [])
        
        prompt = f"""You are an expert technical interviewer conducting a {self.seniority_level} {self.role} interview.

PREVIOUS QUESTION: {previous_q}

USER'S ANSWER: {user_answer}

ANALYSIS: The candidate scored {analysis['technical_depth_score']}/10 on technical depth.
Missing concepts: {', '.join(missing_concepts) if missing_concepts else 'None'}
Strong points: {', '.join(analysis.get('strong_points', []))}

STRATEGY: {strategy}

Generate a follow-up question that:
1. Naturally continues the conversation
2. Tests deeper understanding of weak areas
3. Is not repetitive
4. Maintains interview flow

Return your response in JSON format:
{{
    "question": "The follow-up question",
    "is_drill_down": true,
    "target_concept": "What concept this question targets",
    "ideal_answer": "A comprehensive model answer",
    "difficulty_increase": "higher/same/lower"
}}"""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        follow_up = self._parse_json_response(response.content)
        
        return follow_up
    
    def should_end_interview(self, duration_minutes: int, 
                            questions_asked: int) -> Tuple[bool, str]:
        """
        Determine if interview should end based on time and coverage.
        """
        # End after 10 minutes or 8-10 questions
        if duration_minutes >= 10:
            return True, "Time limit reached"
        
        if questions_asked >= 10:
            return True, "Sufficient questions covered"
        
        # Check if we've covered enough topics
        if len(self.topics_covered) >= 3 and questions_asked >= 6:
            return True, "Good topic coverage achieved"
        
        return False, ""
    
    def generate_transition_question(self, new_topic: str) -> Dict:
        """
        Generate a question to transition to a new topic.
        """
        prompt = f"""You are an expert technical interviewer for a {self.seniority_level} {self.role} position.

We've finished discussing {self.current_topic}. Now transition to: {new_topic}

Generate a smooth transitional question that:
1. Connects to the previous topic if possible
2. Tests knowledge in the new topic
3. Is appropriate for {self.seniority_level} level

Return your response in JSON format:
{{
    "question": "The transitional question",
    "topic": "{new_topic}",
    "ideal_answer": "A comprehensive model answer",
    "key_concepts": ["concept1", "concept2"],
    "transition_phrase": "A natural transition phrase"
}}"""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        result = self._parse_json_response(response.content)
        
        # Update state
        if self.current_topic and self.current_topic not in self.topics_covered:
            self.topics_covered.append(self.current_topic)
        
        self.current_topic = new_topic
        
        return result
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract technical keywords from text.
        """
        prompt = f"""Extract all technical keywords and concepts from this text:

{text}

Return only a JSON array of keywords, like: ["keyword1", "keyword2", "keyword3"]"""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        try:
            keywords = json.loads(response.content.strip())
            return keywords if isinstance(keywords, list) else []
        except:
            return []
    
    def get_knowledge_map(self) -> Dict:
        """
        Return the current knowledge map showing strengths and weaknesses.
        """
        summary = {}
        for topic, data in self.knowledge_map.items():
            avg_score = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0
            summary[topic] = {
                "average_score": round(avg_score, 1),
                "assessment": self._assess_level(avg_score),
                "strong_areas": list(set(data["strong_areas"]))[:3],  # Top 3
                "weak_areas": list(set(data["weak_areas"]))[:3]  # Top 3
            }
        
        return summary
    
    def _assess_level(self, score: float) -> str:
        """Convert score to assessment level."""
        if score >= 8:
            return "Strong"
        elif score >= 6:
            return "Moderate"
        elif score >= 4:
            return "Basic"
        else:
            return "Needs Improvement"
    
    def _parse_json_response(self, text: str) -> Dict:
        """
        Parse JSON from AI response, handling markdown code blocks.
        """
        text = text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        
        if text.endswith("```"):
            text = text[:-3]
        
        text = text.strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"Response text: {text}")
            # Return a fallback
            return {
                "error": "Failed to parse AI response",
                "raw_text": text
            }
    
    def restore_state(self, session_data: Dict):
        """
        Restore conversation state from database.
        """
        self.knowledge_map = session_data.get("knowledge_map", {})
        self.topics_covered = session_data.get("topics_covered", [])
        self.current_topic = session_data.get("current_topic")
        self.follow_up_queue = session_data.get("follow_up_queue", [])
    
    def get_state(self) -> Dict:
        """
        Get current state for persistence.
        """
        return {
            "knowledge_map": self.knowledge_map,
            "topics_covered": self.topics_covered,
            "current_topic": self.current_topic,
            "follow_up_queue": self.follow_up_queue
        }
