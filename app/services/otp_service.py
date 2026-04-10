"""
Stateless OTP Service
=====================

Flow — Generate:
    1. Read rotate_count from DB (otp_state row).
    2. Compute window_id = floor(now / ttl) + rotate_count.
    3. OTP = HMAC(jwt_secret_key, window_id)   ← pure math, NO DB write.
    4. Return OTP string + expires_in + rotate_count (as "version").

Flow — Verify:
    1. Per-user cooldown check (otp_verifications table).
    2. Read current window_id from DB (rotate_count).
    3. Verify HMAC(otp_raw, window_id).
    4. Check otp_verifications: is window_id already used?
       → Yes  : "OTP đã được sử dụng"
       → No   : record verification + increment rotate_count (rotate NOW)
    5. Return success + new expires_in of the NEXT OTP.

Key properties:
  - OTP is NEVER written to DB during generate.
  - DB only gets 1 INSERT per successful verify (audit log row).
  - rotate_count shift makes old OTP invalid for everyone immediately.
  - Unique constraint on window_id prevents concurrent double-use.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import generate_otp_for_window, verify_otp_for_window
from app.crud import crud_otp


class OTPService:

    # ------------------------------------------------------------------
    # Generate (no DB write)
    # ------------------------------------------------------------------

    def generate_otp(
        self, db: Session, issued_by_user_id: str | None = None
    ) -> tuple[str, int, int]:
        """
        Return (otp_raw, expires_in_seconds, rotate_count).
        Does NOT touch the database (except reading rotate_count).
        """
        rotate_count = crud_otp.get_rotate_count(db)
        window_id = crud_otp.current_window_id(rotate_count)
        otp_raw = generate_otp_for_window(window_id)
        expires_in = crud_otp.seconds_until_window_flip()
        return otp_raw, expires_in, rotate_count

    # ------------------------------------------------------------------
    # Verify & rotate (DB write only here)
    # ------------------------------------------------------------------

    def verify_and_rotate(
        self,
        db: Session,
        user_id: str,
        otp_raw: str,
        enforce_cooldown: bool = True,
    ) -> tuple[bool, str, int | None]:
        """
        Returns (valid, message, next_expires_in).
        On success:
          - Writes 1 row to otp_verifications (audit log).
          - Increments rotate_count → new OTP window immediately.
        On failure: zero DB writes.
        """
        now = datetime.now(timezone.utc)

        # 1. Per-user cooldown (read-only, outside heavy transaction)
        if enforce_cooldown:
            last = crud_otp.get_latest_user_verification(db, user_id)
            if last is not None:
                verify_time = (
                    last.created_at.replace(tzinfo=timezone.utc)
                    if last.created_at.tzinfo is None
                    else last.created_at
                )
                elapsed = int((now - verify_time).total_seconds())
                if elapsed < settings.otp_refresh_cooldown_seconds:
                    wait_for = settings.otp_refresh_cooldown_seconds - elapsed
                    return False, f"Bạn đã verify gần đây. Vui lòng thử lại sau {wait_for}s.", None

        # 2. Compute current window (read-only)
        rotate_count = crud_otp.get_rotate_count(db)
        window_id = crud_otp.current_window_id(rotate_count)

        # 3. HMAC check — pure math, no DB
        if not verify_otp_for_window(otp_raw, window_id):
            return False, "OTP không hợp lệ.", None

        # 4. One-time-use check + consume atomically
        #    Use a savepoint so the unique constraint violation is handled cleanly
        #    without rolling back the entire outer transaction (if any).
        try:
            with db.begin_nested():
                if crud_otp.is_window_used(db, window_id):
                    expires_in = crud_otp.seconds_until_window_flip()
                    return False, "OTP này đã được sử dụng. Vui lòng lấy OTP mới từ admin.", expires_in

                # Record usage → unique constraint on window_id prevents races
                crud_otp.record_verification(db, user_id=user_id, window_id=window_id)
                # Increment rotate_count → new HMAC window, old OTP dead immediately
                crud_otp.increment_rotate_count(db)

        except Exception:
            # Unique constraint violation: another request consumed this window first
            expires_in = crud_otp.seconds_until_window_flip()
            return False, "OTP này đã được sử dụng. Vui lòng lấy OTP mới từ admin.", expires_in

        expires_in = crud_otp.seconds_until_window_flip()
        return True, "Xác minh thành công. OTP đã được làm mới ngay lập tức.", expires_in


otp_service = OTPService()
