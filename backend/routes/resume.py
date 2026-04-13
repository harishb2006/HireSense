from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.pdf_parcer import extract_text_from_pdf
from services.resume_analyzer import analyze_skills

router = APIRouter(prefix="/api/resume", tags=["Resume"])

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        text = extract_text_from_pdf(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "filename": file.filename,
        "resume_text": text
    }

@router.post("/analyze")
async def analyze_resume_endpoint(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        text = extract_text_from_pdf(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {str(e)}")

    try:
        result = await analyze_skills(text, job_description)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
