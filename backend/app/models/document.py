from sqlalchemy import Column, Integer, String, Text
from app.db.base_class import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content = Column(Text)
    embedding = Column(Text)  # Store embedding as a comma-separated string
    page = Column(Integer)
    type = Column(String)