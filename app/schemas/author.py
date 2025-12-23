from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class AuthorRead(BaseModel):
    id: UUID
    name: str
    biography: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AuthorCreate(BaseModel):
    name: str
    biography: Optional[str]

class AuthorUpdate(BaseModel):
    name: Optional[str]
    biography: Optional[str]
