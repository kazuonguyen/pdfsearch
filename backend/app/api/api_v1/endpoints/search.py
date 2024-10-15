from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.search import SearchQuery, SearchResponse
from app.services.search_engine import search_knowledge_base

router = APIRouter()

@router.post("/", response_model=SearchResponse)
def search(query: SearchQuery, db: Session = Depends(deps.get_db)):
    results = search_knowledge_base(query.text, db)
    return SearchResponse(results=results)