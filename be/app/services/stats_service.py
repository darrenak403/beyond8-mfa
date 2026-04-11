from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.otp_verification import OTPVerification
from app.models.user import User
from app.schemas.stats import OTPVerificationHistoryItem


class StatsService:
    def get_otp_verification_stats(self, db: Session) -> tuple[int, int]:
        verified_users_stmt = select(func.count(func.distinct(OTPVerification.user_id)))
        total_success_stmt = select(func.count(OTPVerification.id))

        verified_users = db.execute(verified_users_stmt).scalar_one()
        total_success = db.execute(total_success_stmt).scalar_one()

        return int(verified_users or 0), int(total_success or 0)

    def get_otp_verification_history(
        self,
        db: Session,
        *,
        user_id: str | None = None,
    ) -> list[OTPVerificationHistoryItem]:
        stmt = (
            select(
                OTPVerification.user_id,
                User.email,
                func.count(OTPVerification.id).label("verification_count"),
                func.max(OTPVerification.created_at).label("last_verified_at"),
            )
            .join(User, User.id == OTPVerification.user_id)
            .group_by(OTPVerification.user_id, User.email)
            .order_by(func.max(OTPVerification.created_at).desc())
        )

        if user_id:
            stmt = stmt.where(OTPVerification.user_id == user_id)

        rows = db.execute(stmt).all()
        return [
            OTPVerificationHistoryItem(
                user_id=str(row.user_id),
                email=row.email,
                verification_count=int(row.verification_count or 0),
                last_verified_at=row.last_verified_at,
            )
            for row in rows
        ]


stats_service = StatsService()
