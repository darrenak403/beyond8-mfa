from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token, is_course_access_payload_active
from app.crud import crud_user
from app.db.session import get_db
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)
_AUTH_TOKEN_COOKIE_CANDIDATES = ("AUTH_TOKEN_COOKIE", "auth_token")
_COURSE_ACCESS_COOKIE_CANDIDATES = ("beyond8_course_access",)


def _extract_bearer_token(
    credentials: HTTPAuthorizationCredentials | None,
    *,
    detail: str,
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer" or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )
    return credentials.credentials


def _extract_cookie_or_bearer_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None,
    *,
    cookie_names: tuple[str, ...],
    detail: str,
) -> str:
    for cookie_name in cookie_names:
        cookie_token = request.cookies.get(cookie_name)
        if cookie_token:
            return cookie_token
    return _extract_bearer_token(credentials, detail=detail)


def _extract_course_access_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None,
    *,
    detail: str,
) -> str:
    for cookie_name in _COURSE_ACCESS_COOKIE_CANDIDATES:
        cookie_token = request.cookies.get(cookie_name)
        if cookie_token:
            return cookie_token
    # Optional explicit header for clients that cannot send the cookie.
    course_header_token = request.headers.get("x-course-access-token")
    if course_header_token:
        return course_header_token
    return _extract_bearer_token(credentials, detail=detail)


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    token = _extract_cookie_or_bearer_token(
        request,
        credentials,
        cookie_names=_AUTH_TOKEN_COOKIE_CANDIDATES,
        detail=credentials_exception.detail,
    )
    try:
        payload = decode_access_token(token)
        user_id: str | None = payload.get("sub")
        role: str | None = payload.get("role")
        # Keep auth/session token separate from course-access token.
        # course_viewer token must only be accepted by get_current_course_user.
        if user_id is None or role == "course_viewer":
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


def get_current_course_user(
    request: Request,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or revoked course access token",
    )
    token = _extract_course_access_token(
        request,
        credentials,
        detail=credentials_exception.detail,
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
    # Collapse user-not-found and inactive into one 401 response.
    if user is None or not user.is_active:
        raise credentials_exception

    if not is_course_access_payload_active(
        payload,
        expected_course_access_active=user.course_access_active,
        expected_course_access_version=user.course_access_version,
        revoked_at=user.course_access_revoked_at,
    ):
        raise credentials_exception

    return user


def require_course_access(
    current_user: User = Depends(get_current_user),
    course_user: User = Depends(get_current_course_user),
) -> User:
    if course_user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked course access token",
        )
    return current_user
