from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.core.security import create_course_access_token
from app.crud import crud_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.api_response import ApiResponse, success_response
from app.schemas.otp import ExternalOTPVerifyRequest, OTPGenerateResponse, OTPVerifyResponse
from app.services import otp_service

router = APIRouter(prefix="/otp", tags=["OTP"])


@router.get("/generate", response_model=ApiResponse[OTPGenerateResponse])
def generate_otp(admin_user: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    otp, expires_in, version = otp_service.get_or_create_active_otp(db, issued_by_user_id=admin_user.id)
    response_data = OTPGenerateResponse(otp=otp, expires_in=expires_in, version=version)
    return success_response(data=response_data, message="Lấy OTP thành công")


@router.post("/verify", response_model=ApiResponse[OTPVerifyResponse])
def verify_otp(payload: ExternalOTPVerifyRequest, db: Session = Depends(get_db)):
    external_user = crud_user.get_or_create(db, payload.email.lower(), "user")
    valid, message, next_expires = otp_service.verify_and_rotate(
        db,
        user_id=external_user.id,
        otp_raw=payload.otp,
    )
    token = create_course_access_token(subject=external_user.id) if valid else None
    response_data = OTPVerifyResponse(valid=valid, message=message, next_otp_expires_in=next_expires, token=token)
    return success_response(data=response_data, message="Xác minh OTP thành công" if valid else message)
