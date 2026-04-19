from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.schemas.api_response import ApiResponse, success_response
from app.schemas.stats import OTPStatsResponse, OTPVerificationHistoryResponse
from app.services import stats_service

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/otp-verifications", response_model=ApiResponse[OTPStatsResponse])
def otp_verification_stats(_=Depends(get_current_admin), db: Session = Depends(get_db)):
    verified_users, total_key_purchases, total_success = stats_service.get_otp_verification_stats(db)
    response_data = OTPStatsResponse(
        verified_users=verified_users,
        total_key_purchases=total_key_purchases,
        total_successful_verifications=total_success,
    )
    return success_response(data=response_data, message="Lấy thống kê OTP thành công")


@router.get("/otp-verifications/history", response_model=ApiResponse[OTPVerificationHistoryResponse])
def otp_verification_history(
    _=Depends(get_current_admin),
    db: Session = Depends(get_db),
    user_id: str | None = Query(default=None),
):
    items = stats_service.get_otp_verification_history(db, user_id=user_id)
    response_data = OTPVerificationHistoryResponse(total_users=len(items), items=items)
    return success_response(data=response_data, message="Lấy lịch sử verify OTP thành công")
