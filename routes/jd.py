from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.text_cleaner import clean_job_description

router = APIRouter(prefix="/api/jd", tags=["Job Description"])

class JDRequest(BaseModel):
    job_description: str

@router.post("/submit")
async def submit_jd(payload: JDRequest):
    if not payload.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")

    cleaned_jd = clean_job_description(payload.job_description)

    return {
        "cleaned_job_description": cleaned_jd
    }
