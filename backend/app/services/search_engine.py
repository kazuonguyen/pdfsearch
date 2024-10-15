from typing import List
from app.schemas.search import SearchResult
from app.models.document import Document
from app.core.config import settings
from transformers import CLIPProcessor, CLIPModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sqlalchemy.orm import Session

model = CLIPModel.from_pretrained(settings.CLIP_MODEL_NAME)
processor = CLIPProcessor.from_pretrained(settings.CLIP_MODEL_NAME)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def embed_text(text: str):
    inputs = processor(text=text, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        text_features = model.get_text_features(**inputs)
    return text_features.cpu().numpy()

def search_knowledge_base(query: str, db: Session) -> List[SearchResult]:
    # Embed the query
    query_embedding = embed_text(query)

    # Get all documents from the database
    documents = db.query(Document).all()

    results = []
    for doc in documents:
        # Convert the stored embedding string back to a numpy array
        doc_embedding = np.fromstring(doc.embedding, sep=',')
        
        # Calculate cosine similarity
        similarity = cosine_similarity(query_embedding, doc_embedding.reshape(1, -1))[0][0]
        
        results.append(SearchResult(
            type=doc.type,
            content=doc.content[:100] + "..." if len(doc.content) > 100 else doc.content,
            similarity=float(similarity)
        ))

    # Sort results by similarity (highest first)
    results.sort(key=lambda x: x.similarity, reverse=True)

    # Return top 5 results
    return results[:5]