from fastapi import APIRouter
from app.api.api_v1.endpoints import search, document

api_router = APIRouter()
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(document.router, prefix="/documents", tags=["documents"])