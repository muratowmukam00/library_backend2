from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from app.schemas.author import AuthorRead

class BookRead(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    author: Optional[AuthorRead]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class BookCreate(BaseModel):
    title: str
    description: Optional[str]
    author_id: UUID
    category_id: UUID

class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    author_id: Optional[UUID] = None
