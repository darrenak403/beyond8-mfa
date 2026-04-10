from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.schemas.api_response import ApiResponse, success_response
from app.schemas.stats import OTPStatsResponse
from app.services import stats_service

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/otp-verifications", response_model=ApiResponse[OTPStatsResponse])
def otp_verification_stats(_=Depends(get_current_admin), db: Session = Depends(get_db)):
    verified_users, total_success = stats_service.get_otp_verification_stats(db)
    response_data = OTPStatsResponse(
        verified_users=verified_users,
        total_successful_verifications=total_success,
    )
    return success_response(data=response_data, message="Lấy thống kê OTP thành công")
