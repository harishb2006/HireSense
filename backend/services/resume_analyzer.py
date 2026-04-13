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
    You evaluated the candidate's resume mathematically against a job description.
    
    Gaps found (Missing or weak skills compared to requirements):
    {gaps}
    
    Matches (Strong skills):
    {matches}
    
    Based ONLY on this information:
    1. Summarize the biggest gaps in the candidate's profile.
    2. Explain why they are important for the target job description.
    3. Suggest specific ways to rewrite the resume to highlight tangentially related skills OR suggest what exactly to learn to close these gaps.
    
    Keep the response concise, constructive, and actionable. Do not mention mock interviews or the STAR method. Output in markdown format.
    """
    
    response = await llm.ainvoke(prompt)
    
    total = len(matches) + len(gaps)
    match_score = int((len(matches) / total) * 100) if total > 0 else 0

    return {
        "analysis": {
            "match_score": match_score,
            "overall_assessment": response.content,
            "why_not_passing": {
                "main_reasons": ["Resume semantics do not strongly align with certain JD requirements."] if gaps else [],
                "ats_perspective": "Mathematical vector space comparison reveals some missing concepts."
            },
            "missing_keywords": [
                {
                    "keyword": g["jd_requirement"],
                    "importance": "high",
                    "why_matters": f"Semantic match is only {int(g['similarity']*100)}%. Needs better alignment."
                } for g in gaps
            ],
            "gap_analysis": {
                "skills_gaps": "Review the Missing Critical Keywords section for detected vector gaps."
            },
            "actionable_next_steps": [
                "Review the Overall Assessment for detailed LLM feedback.",
                "Iterate on your bullet points to closely match the meaning of the JD requirements."
            ]
        },
        "resumeText": resume_text
    }
