import io
import PyPDF2
from fastapi import UploadFile

async def process_pdf(file: UploadFile) -> str:
    content = await file.read()
    pdf_file = io.BytesIO(content)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    text_content = ""
    for page in pdf_reader.pages:
        text_content += page.extract_text() + "\n"
    
    return text_content