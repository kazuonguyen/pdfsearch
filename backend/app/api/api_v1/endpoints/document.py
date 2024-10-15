from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.document import DocumentCreate, Document as DocumentSchema
from app.crud.crud_document import create_document, get_document
from app.services.pdf_processor import process_pdf

router = APIRouter()

@router.post("/", response_model=DocumentSchema)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db)
):
    if file.filename.endswith('.pdf'):
        content = await process_pdf(file)
        doc_in = DocumentCreate(
            filename=file.filename,
            content=content,
            page=1, 
            type="text"
        )
        document = create_document(db=db, obj_in=doc_in)
        return document
    else:
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

@router.get("/{document_id}", response_model=DocumentSchema)
def read_document(
    document_id: int,
    db: Session = Depends(deps.get_db)
):
    document = get_document(db=db, document_id=document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document