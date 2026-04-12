"""CRUD helpers for per-user stateless OTP."""

import math
from datetime import datetime, timezone

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.otp_verification import OTPVerification
from app.models.user import User


class CRUDOTP:
    def ensure_otp_verification_columns(self, db: Session) -> None:
        db.execute(text("ALTER TABLE otp_verifications ADD COLUMN IF NOT EXISTS otp_rotate_count INTEGER"))

    # ------------------------------------------------------------------
    # Window ID helpers
    # ------------------------------------------------------------------

    def current_window_id(self) -> int:
        """Compute active HMAC window id from current time."""
        now_unix = datetime.now(timezone.utc).timestamp()
        return math.floor(now_unix / settings.otp_ttl_seconds)

    def seconds_until_window_flip(self) -> int:
        """Remaining seconds in the current natural 60-second window."""
        now_unix = datetime.now(timezone.utc).timestamp()
        elapsed = now_unix % settings.otp_ttl_seconds
        return max(1, math.ceil(settings.otp_ttl_seconds - elapsed))

    # ------------------------------------------------------------------
    # Per-user rotation helpers
    # ------------------------------------------------------------------

    def get_user_rotate_count(self, db: Session, user_id: str) -> int:
        stmt = select(User.otp_rotate_count).where(User.id == user_id).limit(1)
        current = db.execute(stmt).scalar_one_or_none()
        if current is None:
            raise ValueError("User not found")
        return int(current)

    def get_user_rotate_count_for_update(self, db: Session, user_id: str) -> int:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .with_for_update(of=User)
            .limit(1)
        )
        user = db.execute(stmt).scalar_one_or_none()
        if user is None:
            raise ValueError("User not found")
        return int(user.otp_rotate_count)

    def increment_user_rotate_count(self, db: Session, user_id: str) -> int:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .with_for_update(of=User)
            .limit(1)
        )
        user = db.execute(stmt).scalar_one_or_none()
        if user is None:
            raise ValueError("User not found")

        user.otp_rotate_count = int(user.otp_rotate_count or 0) + 1
        db.add(user)
        db.flush()
        return int(user.otp_rotate_count)

    def is_counter_used(self, db: Session, user_id: str, otp_rotate_count: int) -> bool:
        stmt = (
            select(OTPVerification)
            .where(OTPVerification.user_id == user_id, OTPVerification.otp_rotate_count == otp_rotate_count)
            .limit(1)
        )
        return db.execute(stmt).scalar_one_or_none() is not None

    def record_verification(
        self,
        db: Session,
        user_id: str,
        window_id: int,
        otp_rotate_count: int,
    ) -> OTPVerification:
        record = OTPVerification(
            user_id=user_id,
            window_id=window_id,
            otp_rotate_count=otp_rotate_count,
            created_at=datetime.now(timezone.utc),
        )
        db.add(record)
        db.flush()
        return record

    # ------------------------------------------------------------------
    # Cooldown helper (per-user rate limiting)
    # ------------------------------------------------------------------

    def get_latest_user_verification(self, db: Session, user_id: str) -> OTPVerification | None:
        from sqlalchemy import desc

        stmt = (
            select(OTPVerification)
            .where(OTPVerification.user_id == user_id)
            .order_by(desc(OTPVerification.created_at))
            .limit(1)
        )
        return db.execute(stmt).scalar_one_or_none()


crud_otp = CRUDOTP()
