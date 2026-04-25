from sqlalchemy.orm import Session

from app.schemas.api_response import success_response
from app.schemas.stats import OTPStatsResponse, OTPVerificationHistoryResponse
from app.services import stats_service


def build_otp_stats_response(db: Session):
    verified_users, total_key_purchases, total_success = stats_service.get_otp_verification_stats(db)
    response_data = OTPStatsResponse(
        verified_users=verified_users,
        total_key_purchases=total_key_purchases,
        total_successful_verifications=total_success,
    )
    return success_response(data=response_data, message="Lấy thống kê OTP thành công")


def build_otp_history_response(db: Session, user_id: str | None = None):
    items = stats_service.get_otp_verification_history(db, user_id=user_id)
    response_data = OTPVerificationHistoryResponse(total_users=len(items), items=items)
    return success_response(data=response_data, message="Lấy lịch sử verify OTP thành công")
