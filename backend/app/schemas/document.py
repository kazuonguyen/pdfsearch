from pydantic import BaseModel

class DocumentBase(BaseModel):
    filename: str
    content: str
    page: int
    type: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int

    class Config:
        orm_mode = True