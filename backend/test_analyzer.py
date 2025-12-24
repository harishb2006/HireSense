#!/usr/bin/env python3
"""
Test script to verify the AI analyzer mentor-style feedback
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from services.ai_analyzer import AIAnalyzer
import json

def test_analyzer():
    print("🧪 Testing HireSense AI Analyzer...\n")
    
    # Sample resume text
    resume_text = """
    John Doe
    Software Engineer
    
    Summary:
    Experienced software engineer with problem-solving skills and team collaboration abilities.
    
    Experience:
    Software Developer at Tech Corp (2020-2023)
    - Developed web applications using React and Node.js
    - Collaborated with team members on various projects
    - Fixed bugs and implemented new features
    
    Skills:
    Python, JavaScript, React, Node.js, Git, SQL
    """
    
    # Sample job description
    job_description = """
    DevOps Engineer - Senior Level
    
    Requirements:
    - 3-5 years of DevOps experience
    - Strong expertise in Docker and Kubernetes
    - Experience with AWS (EC2, ECS, Lambda, S3)
    - CI/CD pipeline development (Jenkins, GitLab CI)
    - Infrastructure as Code (Terraform, CloudFormation)
    - Monitoring tools (Prometheus, Grafana)
    - Microservices architecture experience
    - Strong scripting skills (Python, Bash)
    
    Responsibilities:
    - Design and maintain cloud infrastructure
    - Implement and optimize CI/CD pipelines
    - Monitor and troubleshoot production systems
    - Automate deployment processes
    """
    
    print("📄 Resume: Software Engineer with web development background")
    print("💼 Job: Senior DevOps Engineer role\n")
    print("=" * 60)
    
    analyzer = AIAnalyzer()
    result = analyzer.analyze_resume(resume_text, job_description)
    
    print("\n📊 ANALYSIS RESULTS:\n")
    print(f"Match Score: {result.get('match_score', 'N/A')}%")
    print(f"\nOverall Assessment:\n{result.get('overall_assessment', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("\n🚫 WHY NOT PASSING:\n")
    
    why_not = result.get('why_not_passing', {})
    print("Main Reasons:")
    for i, reason in enumerate(why_not.get('main_reasons', []), 1):
        print(f"  {i}. {reason}")
    
    print(f"\nATS Perspective:\n{why_not.get('ats_perspective', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("\n🔑 MISSING KEYWORDS:\n")
    
    for keyword in result.get('missing_keywords', [])[:3]:  # Show first 3
        print(f"• {keyword['keyword']} ({keyword['importance']})")
        print(f"  Why: {keyword['why_matters']}\n")
    
    print("=" * 60)
    print("\n✅ ACTIONABLE STEPS:\n")
    
    for i, step in enumerate(result.get('actionable_next_steps', []), 1):
        print(f"{i}. {step}\n")
    
    print("=" * 60)
    print("\n✨ Full analysis saved to: test_analysis_output.json")
    
    # Save full output
    with open('test_analysis_output.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    test_analyzer()
