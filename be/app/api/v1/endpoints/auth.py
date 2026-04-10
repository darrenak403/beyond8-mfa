from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.api_response import ApiResponse, success_response
from app.schemas.auth import SignInRequest, TokenResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signin", response_model=ApiResponse[TokenResponse])
def signin(payload: SignInRequest, db: Session = Depends(get_db)):
    token, user = auth_service.signin(db, payload.email)

    response_data = TokenResponse(access_token=token, role=user.role_name, email=user.email)
    return success_response(data=response_data, message="Đăng nhập thành công")


@router.post("/login", response_model=ApiResponse[TokenResponse])
def login_alias(payload: SignInRequest, db: Session = Depends(get_db)):
    return signin(payload, db)
