from pypdf import PdfReader
from fastapi import UploadFile

def extract_text_from_pdf(file: UploadFile) -> str:
    reader = PdfReader(file.file)
    extracted_text = ""

    for page in reader.pages:
        extracted_text += page.extract_text() or ""

    if not extracted_text.strip():
        raise ValueError("No readable text found in PDF")

    return extracted_text
