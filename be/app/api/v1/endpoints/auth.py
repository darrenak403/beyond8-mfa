from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.api_response import ApiResponse, success_response
from app.schemas.auth import SessionStatusResponse, SignInRequest, TokenResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=ApiResponse[bool])
def signup(payload: SignInRequest, db: Session = Depends(get_db)):
    response_ok = auth_service.signup(db, payload.email)
    return success_response(data=response_ok, message="Đăng ký thành công")


@router.post("/login", response_model=ApiResponse[TokenResponse])
def login_alias(payload: SignInRequest, db: Session = Depends(get_db)):
    token, user = auth_service.signin(db, payload.email)
    response_data = TokenResponse(
        access_token=token,
        role=user.role_name,
        email=user.email,
    )
    return success_response(data=response_data, message="Đăng nhập thành công")


@router.get("/session-status", response_model=ApiResponse[SessionStatusResponse])
def session_status(current_user: User = Depends(get_current_user)):
    response_data = SessionStatusResponse(
        user_id=current_user.id,
        email=current_user.email,
        role=current_user.role_name,
        is_active=current_user.is_active,
    )
    return success_response(data=response_data, message="Phiên đăng nhập hợp lệ")
