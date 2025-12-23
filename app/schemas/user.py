from pydantic import BaseModel, EmailStr
from enum import Enum
from uuid import UUID
from typing import Optional
from datetime import datetime

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserRead(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.user

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    role: Optional[UserRole]
