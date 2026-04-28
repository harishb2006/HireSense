import os
import uuid
from langchain_cohere import CohereEmbeddings
from langchain_groq import ChatGroq
from langchain_postgres.vectorstores import PGVector
from langchain_core.documents import Document
from sqlalchemy import create_engine

# Need absolute import according to other files, e.g. "from app.database..." if running from main app
try:
    from app.database.connection import DATABASE_URL
    sync_db_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg://").replace("postgresql://", "postgresql+psycopg://")
except ImportError:
    # Fallback if imported directly
    sync_db_url = os.getenv("DATABASE_URL", "postgresql+psycopg://hiresense_user:hiresense_password@localhost:5433/hiresense_db")
    sync_db_url = sync_db_url.replace("postgresql+asyncpg://", "postgresql+psycopg://").replace("postgresql://", "postgresql+psycopg://")

def get_embeddings():
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY missing in environment variables.")
    # For v3 models we might need to specify input_type depending on the langchain version, usually handled by LangChain or defaults.
    return CohereEmbeddings(cohere_api_key=cohere_api_key, model="embed-english-v3.0")

def get_llm():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY missing in environment variables.")
    # Check for specific model name
    return ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

async def analyze_skills(resume_text: str, jd_text: str):
    """
    Analyzes resume against JD using PGVector for similarity search.
    """
    if not resume_text.strip() or not jd_text.strip():
        raise ValueError("Resume or JD text is empty.")

    llm = get_llm()

    # 1. Extract pure skills from JD using LLM to avoid semantic matching on irrelevant JD text
    jd_extraction_prompt = f"""
    Extract ONLY the core technical skills, tools, and specific hard requirements from this Job Description.
    Return ONLY a comma-separated list of these skills. No bullet points, no explanations, no headers.
    Example output: TypeScript, ReactJS, Python, PostgreSQL, REST APIs, Docker, Git
    
    Job Description:
    {jd_text}
    """
    extracted_jd = await llm.ainvoke(jd_extraction_prompt)
    jd_requirements = [s.strip() for s in extracted_jd.content.split(',') if len(s.strip()) > 2]
    
    # Keep resume chunks naturally so the vector search maps to actual bullet points or sentences
    resume_chunks = [p.strip() for p in resume_text.replace('\n\n', '\n').split('\n') if len(p.strip()) > 10]
    
    if not resume_chunks or not jd_requirements:
        return {"error": "Text too short to extract meaningful chunks."}

    embeddings = get_embeddings()
    collection_name = f"resume_match_{uuid.uuid4().hex}"
    
    # 2. Store Resume in PGVector
    # We create an ephemeral collection for this analysis
    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=sync_db_url,
        use_jsonb=True,
    )
    
    docs = [Document(page_content=chunk) for chunk in resume_chunks]
    vectorstore.add_documents(docs)
    
    # 3. Gap Detection
    matches = []
    gaps = []
    
    for req in jd_requirements:
        # Get closest single match
        results = vectorstore.similarity_search_with_score(req, k=1)
        if results:
            doc, distance = results[0]
            # Convert cosine distance to similarity
            similarity = 1.0 - distance
            # Threshold to consider it a gap (needs tuning in real-world apps)
            if similarity < 0.5:
                gaps.append({"jd_requirement": req, "best_match": doc.page_content, "similarity": round(similarity, 3)})
            else:
                matches.append({"jd_requirement": req, "best_match": doc.page_content, "similarity": round(similarity, 3)})
        else:
            gaps.append({"jd_requirement": req, "best_match": "None", "similarity": 0.0})

    # Clean up the collection since it's merely ephemeral calculation
    try:
        vectorstore.delete_collection()
    except Exception as e:
        print("Warning: failed to delete vector collection:", e)

    # 4. LLM Feedback
    prompt = f"""
    You are an expert technical recruiter and resume analyzer.
    You evaluate candidates holistically, looking for transferrable skills (e.g., MERN/Node.js experience is a strong indicator of backend fundamentals even if Laravel/PHP is missing).
    
    Job Description text: {jd_text}
    
    Resume text: {resume_text}
    
    Strictly vector-based gaps found:
    {gaps}
    
    Strictly vector-based matches:
    {matches}
    
    Based on the FULL Job Description and the FULL Resume text, provide a holistic analysis in JSON format exactly matching this structure:
    {{
        "match_score": 72, 
        "overall_assessment": "You are not a direct Laravel candidate yet, but you are a strong backend transition candidate. The job description clearly states they value backend fundamentals, ability to learn fast, and debugging real code. Your resume already demonstrates many of these through full-stack projects.",
        "strengths": ["Backend Engineering Experience via MERN stack", "Real Product Building (Dashboards, APIs)", "Strong Learning Signals via Hackathons"],
        "why_not_passing_main_reasons": ["Missing specific frameworks like Laravel", "Needs PHP syntax familiarity"],
        "ats_perspective": "You have the fundamental skills but might fail basic keyword filters on Laravel, PHP, Eloquent, and Blade.",
        "missing_keywords_with_context": [
            {{"keyword": "Laravel", "importance": "high", "why_matters": "Core framework for the job, but can be learned quickly given backend foundation."}},
            {{"keyword": "PHP", "importance": "high", "why_matters": "Core language for the job."}}
        ],
        "gap_analysis": {{
            "skills_gaps": "Missing PHP, Laravel framework, Blade templating, Eloquent ORM, and Artisan CLI.",
            "experience_gaps": "No direct PHP/Laravel production deployments or experience with an existing Laravel codebase."
        }},
        "actionable_next_steps": [
            "Day 1: Learn PHP basics: syntax, arrays, functions, OOP.",
            "Day 2: Laravel structure: routes, controllers, views, models.",
            "Day 3: Build a CRUD app with Laravel.",
            "Day 4: Eloquent ORM: queries, relationships, pagination.",
            "Day 5: Blade templates + forms.",
            "Day 6: Artisan + migrations + seeders.",
            "Day 7: Read and debug an existing Laravel GitHub project.",
            "Target resume rewrite: Add keywords like OOP, MVC, Relational Databases, REST API Design. Instead of 'Node.js, Express.js, JWT Auth', use 'Backend Development: Node.js, Express.js, REST APIs, Authentication, MVC Patterns'."
        ]
    }}
    
    Calculate a realistic match_score out of 100. If the candidate lacks specific frameworks but has strong fundamentals and learning velocity (as shown in projects), give them a reasonable passing score (e.g., 60-80%). Do not mention mock interviews.
    Ensure the response is ONLY valid JSON.
    """
    
    # Clean up the collection since it is merely ephemeral calculation
    try:
        vectorstore.delete_collection()
    except Exception as e:
        pass

    response = await llm.ainvoke(prompt)
    import json
    
    try:
        clean_json = response.content.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:-3].strip()
        elif clean_json.startswith("```"):
            clean_json = clean_json[3:-3].strip()
            
        parsed_response = json.loads(clean_json)
        match_score = parsed_response.get("match_score", 50)
        overall_assessment = parsed_response.get("overall_assessment", "")
        strengths = parsed_response.get("strengths", [])
        why_not_passing = {
            "main_reasons": parsed_response.get("why_not_passing_main_reasons", []),
            "ats_perspective": parsed_response.get("ats_perspective", "")
        }
        missing_keywords = parsed_response.get("missing_keywords_with_context", [])
        gap_analysis = parsed_response.get("gap_analysis", {})
        actionable_next_steps = parsed_response.get("actionable_next_steps", [])
        
    except json.JSONDecodeError as e:
        print("JSON Decode Error in resume_analyzer:", e)
        print("Raw response content:", response.content)
        match_score = 65
        overall_assessment = response.content
        strengths = []
        why_not_passing = {"main_reasons": ["LLM failed to output JSON"], "ats_perspective": ""}
        missing_keywords = []
        gap_analysis = {}
        actionable_next_steps = []

    return {
        "analysis": {
            "match_score": match_score,
            "overall_assessment": overall_assessment,
            "strengths": strengths,
            "why_not_passing": why_not_passing,
            "missing_keywords": missing_keywords,
            "gap_analysis": gap_analysis,
            "actionable_next_steps": actionable_next_steps
        },
        "resumeText": resume_text
    }
