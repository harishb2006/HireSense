from pypdf import PdfReader
from fastapi import UploadFile
from io import BytesIO
from typing import Union

def extract_text_from_pdf(file: Union[UploadFile, bytes]) -> str:
    """
    Extract text from a PDF file
    Args:
        file: Either an UploadFile object or bytes content
    Returns:
        Extracted text from all pages
    """
    # Handle both UploadFile and bytes
    if isinstance(file, bytes):
        pdf_file = BytesIO(file)
    else:
        pdf_file = file.file
    
    reader = PdfReader(pdf_file)
    extracted_text = ""

    for page in reader.pages:
        extracted_text += page.extract_text() or ""

    if not extracted_text.strip():
        raise ValueError("No readable text found in PDF")

    return extracted_text
