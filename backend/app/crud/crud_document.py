from sqlalchemy.orm import Session
from app.models.document import Document
from app.schemas.document import DocumentCreate
from app.services.search_engine import embed_text
import numpy as np

def create_document(db: Session, obj_in: DocumentCreate):
    # Embed the document content
    embedding = embed_text(obj_in.content)
    
    # Convert the embedding to a comma-separated string
    embedding_str = ','.join(map(str, embedding.flatten()))

    db_obj = Document(
        filename=obj_in.filename,
        content=obj_in.content,
        embedding=embedding_str,
        page=obj_in.page,
        type=obj_in.type
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_document(db: Session, document_id: int):
    return db.query(Document).filter(Document.id == document_id).first()