from uuid import UUID

from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryRead(CategoryBase):
    id: UUID

    model_config = {
        "from_attributes": True
    }
