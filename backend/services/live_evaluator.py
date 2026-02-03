"""
Live Evaluator Service - Real-time Interview Scoring
Tracks technical depth, clarity, and confidence during conversations
"""

import re
from typing import Dict, List
import os


class LiveEvaluator:
    """
    Evaluates user responses in real-time without breaking interview immersion.
    Provides continuous feedback on technical depth, clarity, and confidence.
    """
    
    def __init__(self):
        self.cumulative_scores = {
            "technical_depth": [],
            "clarity": [],
            "confidence": []
        }
    
    def evaluate_response(self, question: str, user_answer: str, 
                         ideal_answer: str = None) -> Dict:
        """
        Evaluate a single user response across all dimensions.
        """
        # Quick evaluation for live feedback
        technical_depth = self._evaluate_technical_depth(user_answer, ideal_answer)
        clarity = self._evaluate_clarity(user_answer)
        confidence = self._evaluate_confidence(user_answer)
        
        # Store scores
        self.cumulative_scores["technical_depth"].append(technical_depth)
        self.cumulative_scores["clarity"].append(clarity)
        self.cumulative_scores["confidence"].append(confidence)
        
        return {
            "technical_depth_score": round(technical_depth, 1),
            "clarity_score": round(clarity, 1),
            "confidence_score": round(confidence, 1),
            "overall_score": round((technical_depth + clarity + confidence) / 3, 1)
        }
    
    def _evaluate_technical_depth(self, answer: str, ideal_answer: str = None) -> float:
        """
        Evaluate technical depth based on:
        - Use of technical terms
        - Explanation complexity
        - Code examples or specific references
        """
        score = 5.0  # Base score
        
        # Technical keywords (positive indicators)
        technical_patterns = [
            r'\b(algorithm|architecture|design pattern|implementation|optimization)\b',
            r'\b(async|synchronous|concurrent|parallel|thread)\b',
            r'\b(database|query|index|schema|transaction)\b',
            r'\b(API|REST|GraphQL|endpoint|middleware)\b',
            r'\b(state|props|lifecycle|hook|component)\b',
            r'\b(closure|callback|promise|event loop|prototype)\b'
        ]
        
        technical_count = sum(
            len(re.findall(pattern, answer.lower())) 
            for pattern in technical_patterns
        )
        
        # Add points for technical terms (max +3)
        score += min(technical_count * 0.3, 3.0)
        
        # Check for code examples or specific syntax
        if '```' in answer or re.search(r'[{}\[\]();]', answer):
            score += 1.0
        
        # Check for explanations (using words like "because", "due to", "since")
        explanation_words = ['because', 'due to', 'since', 'this means', 'therefore', 'as a result']
        if any(word in answer.lower() for word in explanation_words):
            score += 0.5
        
        # Penalize very short answers (less than 50 chars)
        if len(answer) < 50:
            score -= 2.0
        
        # Penalize vague answers
        vague_words = ['maybe', 'i think', 'not sure', "don't know", 'possibly']
        vague_count = sum(1 for word in vague_words if word in answer.lower())
        score -= vague_count * 0.5
        
        return max(0, min(10, score))
    
    def _evaluate_clarity(self, answer: str) -> float:
        """
        Evaluate clarity based on:
        - Structure (paragraphs, bullet points)
        - Grammar and readability
        - Logical flow
        """
        score = 5.0
        
        # Check for structured answer
        if '\n' in answer or '1.' in answer or '•' in answer or '-' in answer:
            score += 1.5
        
        # Check sentence count (good answers have multiple sentences)
        sentences = [s.strip() for s in answer.split('.') if s.strip()]
        if len(sentences) >= 3:
            score += 1.0
        elif len(sentences) == 1:
            score -= 1.0
        
        # Check for connector words (shows logical flow)
        connectors = ['first', 'second', 'then', 'next', 'finally', 'however', 
                     'therefore', 'additionally', 'furthermore', 'moreover']
        connector_count = sum(1 for word in connectors if word in answer.lower())
        score += min(connector_count * 0.5, 2.0)
        
        # Penalize run-on answers (very long without structure)
        if len(answer) > 500 and answer.count('\n') < 2:
            score -= 1.0
        
        # Penalize excessive filler words
        fillers = ['like', 'um', 'uh', 'basically', 'actually', 'literally']
        filler_count = sum(answer.lower().count(word) for word in fillers)
        score -= min(filler_count * 0.3, 2.0)
        
        return max(0, min(10, score))
    
    def _evaluate_confidence(self, answer: str) -> float:
        """
        Evaluate confidence based on:
        - Definitive statements vs hedging
        - Use of assertive language
        - Completeness of answer
        """
        score = 5.0
        
        # Confident indicators
        confident_words = [
            'definitely', 'certainly', 'absolutely', 'precisely', 
            'exactly', 'always', 'never', 'must', 'will', 'is', 'does'
        ]
        confident_count = sum(1 for word in confident_words if word in answer.lower())
        score += min(confident_count * 0.3, 2.0)
        
        # Uncertain indicators (penalties)
        uncertain_words = [
            'maybe', 'perhaps', 'possibly', 'might', 'could', 'i think',
            'i guess', 'probably', 'not sure', "don't know", 'uncertain'
        ]
        uncertain_count = sum(1 for word in uncertain_words if word in answer.lower())
        score -= uncertain_count * 0.7
        
        # Question marks in answer (shows uncertainty)
        score -= answer.count('?') * 0.5
        
        # Complete sentences show confidence
        if answer.endswith('.') or answer.endswith('!'):
            score += 0.5
        
        # Length as proxy for confidence (very short = less confident)
        if len(answer) < 30:
            score -= 2.0
        elif len(answer) > 100:
            score += 1.0
        
        return max(0, min(10, score))
    
    def get_cumulative_scores(self) -> Dict:
        """
        Get average scores across all responses.
        """
        return {
            "technical_depth": round(
                sum(self.cumulative_scores["technical_depth"]) / 
                len(self.cumulative_scores["technical_depth"]) 
                if self.cumulative_scores["technical_depth"] else 0, 1
            ),
            "clarity": round(
                sum(self.cumulative_scores["clarity"]) / 
                len(self.cumulative_scores["clarity"]) 
                if self.cumulative_scores["clarity"] else 0, 1
            ),
            "confidence": round(
                sum(self.cumulative_scores["confidence"]) / 
                len(self.cumulative_scores["confidence"]) 
                if self.cumulative_scores["confidence"] else 0, 1
            )
        }
    
    def get_overall_score(self) -> float:
        """
        Calculate overall interview score.
        """
        cumulative = self.get_cumulative_scores()
        overall = (
            cumulative["technical_depth"] + 
            cumulative["clarity"] + 
            cumulative["confidence"]
        ) / 3
        return round(overall, 1)
    
    def get_performance_trend(self) -> Dict:
        """
        Analyze if candidate is improving or declining over time.
        """
        tech_scores = self.cumulative_scores["technical_depth"]
        
        if len(tech_scores) < 3:
            return {"trend": "insufficient_data"}
        
        # Compare first half vs second half
        mid = len(tech_scores) // 2
        first_half_avg = sum(tech_scores[:mid]) / mid
        second_half_avg = sum(tech_scores[mid:]) / (len(tech_scores) - mid)
        
        diff = second_half_avg - first_half_avg
        
        if diff > 1.0:
            trend = "improving"
        elif diff < -1.0:
            trend = "declining"
        else:
            trend = "consistent"
        
        return {
            "trend": trend,
            "first_half_avg": round(first_half_avg, 1),
            "second_half_avg": round(second_half_avg, 1),
            "difference": round(diff, 1)
        }
    
    def generate_live_feedback_hint(self, latest_score: Dict) -> str:
        """
        Generate subtle hints for improvement without breaking immersion.
        (Optional - can be shown after interview)
        """
        hints = []
        
        if latest_score["technical_depth_score"] < 5:
            hints.append("Try to provide more technical details and specific examples")
        
        if latest_score["clarity_score"] < 5:
            hints.append("Structure your answer with clear points or steps")
        
        if latest_score["confidence_score"] < 5:
            hints.append("Be more assertive in your explanations")
        
        return " | ".join(hints) if hints else "Keep going!"
