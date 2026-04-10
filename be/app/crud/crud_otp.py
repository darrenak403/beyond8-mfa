"""
CRUD helpers for the stateless OTP system.

Window ID formula:
    window_id = floor(unix_timestamp / otp_ttl_seconds) + rotate_count

- rotate_count is stored in the singleton otp_state row (id=1).
- Each successful OTP verification atomically increments rotate_count,
  which immediately invalidates the current OTP string for everyone else.
- The OTP value itself is NEVER stored in the database; it is derived
  on-the-fly from HMAC(jwt_secret_key, window_id).
"""

import math
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.otp_state import OTPState
from app.models.otp_verification import OTPVerification


class CRUDOTP:
    # ------------------------------------------------------------------
    # OTPState (singleton) helpers
    # ------------------------------------------------------------------

    def _ensure_state_row(self, db: Session) -> OTPState:
        """Return the singleton state row, creating it if it doesn't exist."""
        state = db.get(OTPState, 1)
        if state is None:
            state = OTPState(id=1, rotate_count=0, updated_at=datetime.now(timezone.utc))
            db.add(state)
            db.flush()
        return state

    def get_rotate_count(self, db: Session) -> int:
        state = self._ensure_state_row(db)
        return state.rotate_count

    def increment_rotate_count(self, db: Session) -> int:
        """Atomically increment rotate_count and return the NEW value."""
        state = self._ensure_state_row(db)
        state.rotate_count += 1
        state.updated_at = datetime.now(timezone.utc)
        db.add(state)
        db.flush()
        return state.rotate_count

    # ------------------------------------------------------------------
    # Window ID helpers
    # ------------------------------------------------------------------

    def current_window_id(self, rotate_count: int) -> int:
        """
        Compute the active HMAC window id.
        Changes both on the regular TTL tick AND after each rotate.
        """
        now_unix = datetime.now(timezone.utc).timestamp()
        base = math.floor(now_unix / settings.otp_ttl_seconds)
        return base + rotate_count

    def seconds_until_window_flip(self) -> int:
        """Remaining seconds in the current natural 60-second window."""
        now_unix = datetime.now(timezone.utc).timestamp()
        elapsed = now_unix % settings.otp_ttl_seconds
        return max(1, math.ceil(settings.otp_ttl_seconds - elapsed))

    # ------------------------------------------------------------------
    # Used-window helpers  (one-time-use enforcement)
    # ------------------------------------------------------------------

    def is_window_used(self, db: Session, window_id: int) -> bool:
        stmt = select(OTPVerification).where(OTPVerification.window_id == window_id).limit(1)
        return db.execute(stmt).scalar_one_or_none() is not None

    def record_verification(self, db: Session, user_id: str, window_id: int) -> OTPVerification:
        """Persist the successful OTP usage — this is the ONLY DB write for an OTP lifecycle."""
        record = OTPVerification(
            user_id=user_id,
            window_id=window_id,
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
