from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.api_response import ApiResponse, success_response
from app.schemas.auth import RefreshTokenRequest, SessionStatusResponse, SignInRequest, TokenResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signin", response_model=ApiResponse[TokenResponse])
def signin(payload: SignInRequest, db: Session = Depends(get_db)):
    token, refresh_token, expires_in, user = auth_service.signin(db, payload.email)

    response_data = TokenResponse(
        access_token=token,
        refresh_token=refresh_token,
        expires_in=expires_in,
        role=user.role_name,
        email=user.email,
    )
    return success_response(data=response_data, message="Đăng nhập thành công")


@router.post("/login", response_model=ApiResponse[TokenResponse])
def login_alias(payload: SignInRequest, db: Session = Depends(get_db)):
    return signin(payload, db)


@router.post("/refresh-token", response_model=ApiResponse[TokenResponse])
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    token, new_refresh_token, expires_in, user = auth_service.refresh_access_token(db, payload.refresh_token)
    response_data = TokenResponse(
        access_token=token,
        refresh_token=new_refresh_token,
        expires_in=expires_in,
        role=user.role_name,
        email=user.email,
    )
    return success_response(data=response_data, message="Làm mới phiên đăng nhập thành công")


@router.get("/session-status", response_model=ApiResponse[SessionStatusResponse])
def session_status(current_user: User = Depends(get_current_user)):
    response_data = SessionStatusResponse(
        user_id=current_user.id,
        email=current_user.email,
        role=current_user.role_name,
        is_active=current_user.is_active,
    )
    return success_response(data=response_data, message="Phiên đăng nhập hợp lệ")
