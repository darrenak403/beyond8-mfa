from datetime import datetime

from pydantic import BaseModel, EmailStr


class SignInRequest(BaseModel):
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    email: EmailStr


class UserItemResponse(BaseModel):
    id: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime


class UserListResponse(BaseModel):
    total_users: int
    offset: int
    limit: int
    users: list[UserItemResponse]
