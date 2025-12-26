from pydantic import BaseModel, EmailStr, constr
from enum import Enum
from uuid import UUID
from typing import Optional
from datetime import datetime

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserRead(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password:  constr(min_length=8, max_length=50)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
