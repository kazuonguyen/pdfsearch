from pydantic import BaseModel
from typing import List

class SearchQuery(BaseModel):
    text: str

class SearchResult(BaseModel):
    type: str
    content: str
    similarity: float

class SearchResponse(BaseModel):
    results: List[SearchResult]