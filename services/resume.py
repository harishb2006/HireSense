from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_parser import extract_text_from_pdf

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
