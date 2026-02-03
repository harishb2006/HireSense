"""
Interview Analyzer - Post-Interview Debrief and Report Generation
Generates detailed reports comparing user answers to model answers
Uses Cerebras AI (Llama models) via LangChain
"""

import os
import json
from typing import Dict, List
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage


class InterviewAnalyzer:
    """
    Generates comprehensive post-interview reports with:
    - Transcript vs Model Answers comparison
    - Knowledge map visualization data
    - Strengths and weaknesses breakdown
    - Improvement recommendations
    """
    
    def __init__(self):
        # Initialize Cerebras AI via LangChain
        self.model = ChatOpenAI(
            base_url="https://api.cerebras.ai/v1",
            api_key=os.environ.get("CEREBRAS_API_KEY"),
            model=os.environ.get("CEREBRAS_MODEL", "llama-3.3-70b"),
            temperature=0.7
        )
    
    def generate_debrief_report(self, session_data: Dict, 
                               conversation_history: List[Dict]) -> Dict:
        """
        Generate comprehensive debrief report after interview completion.
        """
        # Extract Q&A pairs
        qa_pairs = self._extract_qa_pairs(conversation_history)
        
        # Generate detailed analysis
        analysis = self._analyze_overall_performance(qa_pairs, session_data)
        
        # Generate improvement recommendations
        recommendations = self._generate_recommendations(
            session_data.get("knowledge_map", {}),
            analysis
        )
        
        return {
            "session_id": session_data["session_id"],
            "candidate_info": {
                "role": session_data["role"],
                "seniority_level": session_data["seniority_level"],
                "duration_minutes": session_data.get("duration_minutes", 0)
            },
            "overall_scores": {
                "total_score": session_data.get("total_score", 0),
                "technical_depth": session_data.get("technical_depth_score", 0),
                "clarity": session_data.get("clarity_score", 0),
                "confidence": session_data.get("confidence_score", 0)
            },
            "performance_analysis": analysis,
            "knowledge_map": session_data.get("knowledge_map", {}),
            "qa_comparisons": self._generate_qa_comparisons(qa_pairs),
            "strengths": analysis.get("strengths", []),
            "weaknesses": analysis.get("weaknesses", []),
            "recommendations": recommendations,
            "transcript": qa_pairs
        }
    
    def _extract_qa_pairs(self, conversation_history: List[Dict]) -> List[Dict]:
        """
        Extract question-answer pairs from conversation history.
        """
        qa_pairs = []
        current_question = None
        
        for i, msg in enumerate(conversation_history):
            if msg["role"] == "assistant":
                current_question = {
                    "question": msg["message"],
                    "question_number": (i // 2) + 1,
                    "topic": msg.get("topic"),
                    "model_answer": msg.get("model_answer"),
                    "is_follow_up": msg.get("is_follow_up") == "true"
                }
            elif msg["role"] == "user" and current_question:
                current_question["user_answer"] = msg["message"]
                current_question["scores"] = {
                    "technical_depth": msg.get("depth_score"),
                    "clarity": msg.get("clarity_score"),
                    "confidence": msg.get("confidence_score")
                }
                current_question["keywords"] = msg.get("keywords_detected", [])
                qa_pairs.append(current_question)
                current_question = None
        
        return qa_pairs
    
    def _analyze_overall_performance(self, qa_pairs: List[Dict], 
                                    session_data: Dict) -> Dict:
        """
        Generate overall performance analysis using AI.
        """
        # Prepare summary of performance
        summary_text = f"""Interview Performance Summary:
Role: {session_data['role']}
Seniority Level: {session_data['seniority_level']}
Total Questions: {len(qa_pairs)}
Average Scores:
- Technical Depth: {session_data.get('technical_depth_score', 0)}/10
- Clarity: {session_data.get('clarity_score', 0)}/10
- Confidence: {session_data.get('confidence_score', 0)}/10

Topics Covered: {', '.join(session_data.get('topics_covered', []))}

Question-Answer Performance:
"""
        
        for qa in qa_pairs[:5]:  # Analyze first 5 Q&As for summary
            summary_text += f"\nQ: {qa['question'][:100]}..."
            summary_text += f"\nA: {qa['user_answer'][:150]}..."
            summary_text += f"\nScores: Depth={qa['scores']['technical_depth']}, Clarity={qa['scores']['clarity']}\n"
        
        prompt = f"""{summary_text}

As an expert technical interviewer, analyze this candidate's overall performance and provide:

1. Key Strengths (3-5 specific points)
2. Key Weaknesses (3-5 specific points)
3. Overall Assessment (paragraph summarizing readiness for the role)
4. Pattern Analysis (did they improve, decline, or stay consistent?)

Return your analysis in JSON format:
{{
    "strengths": ["strength1", "strength2", "strength3"],
    "weaknesses": ["weakness1", "weakness2", "weakness3"],
    "overall_assessment": "Detailed paragraph assessment",
    "performance_trend": "improving/declining/consistent",
    "readiness_level": "ready/needs_practice/needs_significant_improvement",
    "standout_moment": "Description of best answer or insight",
    "concerning_moment": "Description of worst answer or gap"
}}"""
        
        messages = [HumanMessage(content=prompt)]
        response = self.model.invoke(messages)
        analysis = self._parse_json_response(response.content)
        
        return analysis
    
    def _generate_qa_comparisons(self, qa_pairs: List[Dict]) -> List[Dict]:
        """
        Generate side-by-side comparisons of user answers vs model answers.
        """
        comparisons = []
        
        for qa in qa_pairs:
            comparison = {
                "question_number": qa["question_number"],
                "question": qa["question"],
                "topic": qa.get("topic"),
                "is_follow_up": qa.get("is_follow_up", False),
                "user_answer": qa["user_answer"],
                "model_answer": qa.get("model_answer", "Not available"),
                "scores": qa["scores"],
                "keywords_used": qa.get("keywords", []),
                "gap_analysis": self._analyze_answer_gap(
                    qa["user_answer"],
                    qa.get("model_answer"),
                    qa["scores"]
                )
            }
            comparisons.append(comparison)
        
        return comparisons
    
    def _analyze_answer_gap(self, user_answer: str, model_answer: str, 
                           scores: Dict) -> Dict:
        """
        Analyze the gap between user answer and model answer.
        """
        if not model_answer or model_answer == "Not available":
            return {
                "gap_size": "unknown",
                "missing_concepts": [],
                "what_to_improve": "Model answer not available"
            }
        
        # Quick analysis
        if scores["technical_depth"] >= 8:
            gap = "minimal"
            improvement = "Answer was strong, minor refinements possible"
        elif scores["technical_depth"] >= 6:
            gap = "moderate"
            improvement = "Good understanding, could add more depth and examples"
        else:
            gap = "significant"
            improvement = "Needs to study this topic more thoroughly"
        
        return {
            "gap_size": gap,
            "what_to_improve": improvement,
            "score_breakdown": scores
        }
    
    def _generate_recommendations(self, knowledge_map: Dict, 
                                 analysis: Dict) -> List[Dict]:
        """
        Generate personalized improvement recommendations.
        """
        recommendations = []
        
        # Analyze knowledge map for weak areas
        weak_topics = []
        for topic, data in knowledge_map.items():
            if data.get("average_score", 10) < 6:
                weak_topics.append({
                    "topic": topic,
                    "score": data.get("average_score", 0),
                    "weak_areas": data.get("weak_areas", [])
                })
        
        # Sort by score (weakest first)
        weak_topics.sort(key=lambda x: x["score"])
        
        # Generate recommendations for top 3 weak topics
        for topic_data in weak_topics[:3]:
            topic = topic_data["topic"]
            weak_areas = topic_data["weak_areas"]
            
            rec = {
                "priority": "high" if topic_data["score"] < 4 else "medium",
                "topic": topic,
                "current_level": self._score_to_level(topic_data["score"]),
                "focus_areas": weak_areas[:3] if weak_areas else ["Core concepts"],
                "suggested_resources": self._suggest_resources(topic, weak_areas),
                "practice_questions": self._suggest_practice(topic)
            }
            recommendations.append(rec)
        
        # Add strength-based recommendations
        if "strengths" in analysis:
            strengths = analysis["strengths"]
            if strengths:
                recommendations.append({
                    "priority": "maintain",
                    "topic": "Strengths to Maintain",
                    "current_level": "strong",
                    "focus_areas": strengths[:2],
                    "suggestion": "Keep practicing these areas to maintain your advantage"
                })
        
        return recommendations
    
    def _score_to_level(self, score: float) -> str:
        """Convert numeric score to level description."""
        if score >= 8:
            return "Advanced"
        elif score >= 6:
            return "Intermediate"
        elif score >= 4:
            return "Basic"
        else:
            return "Beginner"
    
    def _suggest_resources(self, topic: str, weak_areas: List[str]) -> List[str]:
        """
        Suggest learning resources based on topic and weak areas.
        """
        # Generic suggestions (in production, this could be more sophisticated)
        resources = [
            f"Official documentation for {topic}",
            f"Advanced tutorials on {topic}",
            "Practice problems and coding challenges"
        ]
        
        if weak_areas:
            resources.insert(0, f"Focus on: {', '.join(weak_areas[:2])}")
        
        return resources
    
    def _suggest_practice(self, topic: str) -> List[str]:
        """Suggest practice questions for improvement."""
        return [
            f"Build a small project using {topic}",
            f"Explain {topic} to someone else",
            f"Review {topic} implementation in open-source projects"
        ]
    
    def generate_html_report(self, report_data: Dict) -> str:
        """
        Generate HTML version of the report for better visualization.
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Interview Report - {report_data['session_id'][:8]}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
                h2 {{ color: #34495e; margin-top: 30px; }}
                .score-card {{ display: inline-block; background: #ecf0f1; padding: 20px; margin: 10px; border-radius: 8px; min-width: 200px; }}
                .score-value {{ font-size: 36px; font-weight: bold; color: #3498db; }}
                .strength {{ color: #27ae60; }}
                .weakness {{ color: #e74c3c; }}
                .qa-pair {{ background: #f8f9fa; padding: 20px; margin: 15px 0; border-left: 4px solid #3498db; border-radius: 4px; }}
                .model-answer {{ background: #d5f4e6; padding: 15px; margin-top: 10px; border-radius: 4px; }}
                .recommendation {{ background: #fff3cd; padding: 15px; margin: 10px 0; border-radius: 4px; border-left: 4px solid #ffc107; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Interview Performance Report</h1>
                <p><strong>Role:</strong> {report_data['candidate_info']['role']}</p>
                <p><strong>Level:</strong> {report_data['candidate_info']['seniority_level']}</p>
                <p><strong>Duration:</strong> {report_data['candidate_info']['duration_minutes']} minutes</p>
                
                <h2>Overall Scores</h2>
                <div class="score-card">
                    <div>Total Score</div>
                    <div class="score-value">{report_data['overall_scores']['total_score']}/10</div>
                </div>
                <div class="score-card">
                    <div>Technical Depth</div>
                    <div class="score-value">{report_data['overall_scores']['technical_depth']}/10</div>
                </div>
                <div class="score-card">
                    <div>Clarity</div>
                    <div class="score-value">{report_data['overall_scores']['clarity']}/10</div>
                </div>
                <div class="score-card">
                    <div>Confidence</div>
                    <div class="score-value">{report_data['overall_scores']['confidence']}/10</div>
                </div>
                
                <h2>Strengths</h2>
                <ul>
                    {"".join(f'<li class="strength">{s}</li>' for s in report_data.get('strengths', []))}
                </ul>
                
                <h2>Areas for Improvement</h2>
                <ul>
                    {"".join(f'<li class="weakness">{w}</li>' for w in report_data.get('weaknesses', []))}
                </ul>
                
                <h2>Personalized Recommendations</h2>
                {"".join(f'<div class="recommendation"><strong>{r["topic"]}</strong> - Priority: {r["priority"]}<br>Focus on: {", ".join(r.get("focus_areas", []))}</div>' for r in report_data.get('recommendations', []))}
                
                <h2>Question-Answer Review</h2>
                {"".join(self._format_qa_html(qa) for qa in report_data.get('qa_comparisons', [])[:5])}
            </div>
        </body>
        </html>
        """
        return html
    
    def _format_qa_html(self, qa: Dict) -> str:
        """Format a single Q&A pair as HTML."""
        return f"""
        <div class="qa-pair">
            <h3>Question {qa['question_number']}: {qa['topic'] or 'General'}</h3>
            <p><strong>Q:</strong> {qa['question']}</p>
            <p><strong>Your Answer:</strong> {qa['user_answer']}</p>
            <div class="model-answer">
                <strong>Model Answer:</strong> {qa.get('model_answer', 'N/A')[:300]}...
            </div>
            <p><strong>Scores:</strong> Depth: {qa['scores']['technical_depth']}, 
               Clarity: {qa['scores']['clarity']}, 
               Confidence: {qa['scores']['confidence']}</p>
        </div>
        """
    
    def _parse_json_response(self, text: str) -> Dict:
        """Parse JSON from AI response."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"error": "Failed to parse response", "raw": text}
