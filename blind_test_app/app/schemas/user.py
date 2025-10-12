import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.db.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole
    name: str
    surname: str
    phone: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserSignup(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str
    phone: Optional[str] = None


class JudgeCreate(BaseModel):
    email: EmailStr
    name: str
    surname: str
    phone: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    id: uuid.UUID
    password_hash: str
    created_at: datetime
    created_by_admin_id: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
    created_by_admin_id: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    email: Optional[str] = None
