from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token, is_course_access_payload_active
from app.crud import crud_user
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = decode_access_token(token)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = crud_user.get_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị khóa",
        )

    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role_name != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return current_user


def get_current_course_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or revoked course access token",
    )
    try:
        payload = decode_access_token(token)
        user_id: str | None = payload.get("sub")
        role: str | None = payload.get("role")
        if user_id is None or role != "course_viewer":
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = crud_user.get_by_id(db, user_id)
    if user is None or not user.is_active:
        raise credentials_exception

    if not is_course_access_payload_active(
        payload,
        expected_course_access_version=user.course_access_version,
        revoked_at=user.course_access_revoked_at,
    ):
        raise credentials_exception

    return user
