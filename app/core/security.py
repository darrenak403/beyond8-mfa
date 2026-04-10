from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import jwt
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from app.core.config import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def create_access_token(subject: str, role: str) -> str:
    payload: Dict[str, Any] = {
        "sub": subject,
        "role": role,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_course_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.course_access_token_expire_days)
    payload: Dict[str, Any] = {
        "sub": subject,
        "role": "course_viewer",
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


def hash_value(raw_value: str) -> str:
    return pwd_context.hash(raw_value)


def verify_hash(raw_value: str, hashed_value: str) -> bool:
    try:
        return pwd_context.verify(raw_value, hashed_value)
    except (ValueError, UnknownHashError):
        return False
