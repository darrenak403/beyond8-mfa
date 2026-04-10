from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_current_user
from app.core.security import create_course_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.api_response import ApiResponse, success_response
from app.schemas.otp import ExternalOTPVerifyRequest, OTPGenerateResponse, OTPVerifyResponse
from app.services import otp_service

router = APIRouter(prefix="/otp", tags=["OTP"])


@router.get("/generate", response_model=ApiResponse[OTPGenerateResponse])
def generate_otp(admin_user: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Generate current active OTP for admin to share.
    Does NOT write anything to the database — purely stateless HMAC computation.
    """
    otp, expires_in, version = otp_service.generate_otp(db, issued_by_user_id=admin_user.id)
    response_data = OTPGenerateResponse(otp=otp, expires_in=expires_in, version=version)
    return success_response(data=response_data, message="Lấy OTP thành công")


@router.post("/verify", response_model=ApiResponse[OTPVerifyResponse])
def verify_otp(
    payload: ExternalOTPVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Verify OTP submitted by an authenticated user.
    On success: records audit log row + immediately rotates OTP window.
    On failure: no DB writes.
    """
    if payload.email.lower().strip() != current_user.email.lower().strip():
        response_data = OTPVerifyResponse(
            valid=False,
            message="Email không khớp với người dùng đang đăng nhập",
            next_otp_expires_in=None,
            token=None,
        )
        return success_response(data=response_data, message="Email không hợp lệ")

    valid, message, next_expires = otp_service.verify_and_rotate(
        db,
        user_id=current_user.id,
        otp_raw=payload.otp,
    )
    token = create_course_access_token(subject=current_user.id) if valid else None
    response_data = OTPVerifyResponse(valid=valid, message=message, next_otp_expires_in=next_expires, token=token)
    return success_response(data=response_data, message="Xác minh OTP thành công" if valid else message)
