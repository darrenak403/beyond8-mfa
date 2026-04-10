from sqlalchemy import distinct, func, select
from sqlalchemy.orm import Session

from app.models.otp_verification import OTPVerification


class StatsService:
    def get_otp_verification_stats(self, db: Session) -> tuple[int, int]:
        verified_users_stmt = select(func.count(OTPVerification.user_id))
        total_success_stmt = select(func.count(OTPVerification.id))

        verified_users = db.execute(verified_users_stmt).scalar_one()
        total_success = db.execute(total_success_stmt).scalar_one()

        return int(verified_users or 0), int(total_success or 0)


stats_service = StatsService()
