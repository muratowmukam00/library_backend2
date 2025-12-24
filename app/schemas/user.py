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
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class UserCreate(BaseModel):
    email: EmailStr
    password:  constr(min_length=8, max_length=50)
    role: Optional[UserRole] = UserRole.user

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    role: Optional[UserRole]
