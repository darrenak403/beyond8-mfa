from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class SignInRequest(BaseModel):
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"
    role: str
    email: EmailStr


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(min_length=16, max_length=255)


class SessionStatusResponse(BaseModel):
    user_id: str
    email: EmailStr
    role: str
    is_active: bool


class UserItemResponse(BaseModel):
    id: str
    email: EmailStr
    role: str
    is_active: bool
    blocked_at: datetime | None = None
    blocked_reason: str | None = None
    blocked_by_user_id: str | None = None
    created_at: datetime


class BlockUserRequest(BaseModel):
    reason: str | None = Field(default=None, max_length=255)


class UserListResponse(BaseModel):
    total_users: int
    offset: int
    limit: int
    users: list[UserItemResponse]
