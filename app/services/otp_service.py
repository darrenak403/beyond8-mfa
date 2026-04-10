import secrets
from contextlib import contextmanager
from datetime import datetime, timezone

from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.core.config import settings
from app.crud import crud_otp
from app.models.otp_verification import OTPVerification

SAFE_CHARS = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


class OTPService:
    _LOCK_KEY = 814208

    @contextmanager
    def _transaction(self, db: Session):
        if db.in_transaction():
            yield
            return

        with db.begin():
            yield

    def _generate_raw_otp(self) -> str:
        random_chars = "".join(secrets.choice(SAFE_CHARS) for _ in range(12))
        return f"{settings.key_prefix}-{random_chars[0:4]}-{random_chars[4:8]}-{random_chars[8:12]}"

    def _seconds_until_expiry(self, expires_at: datetime) -> int:
        expiry = expires_at.replace(tzinfo=timezone.utc) if expires_at.tzinfo is None else expires_at
        return max(0, int((expiry - datetime.now(timezone.utc)).total_seconds()))

    def get_or_create_active_otp(self, db: Session, issued_by_user_id: str | None = None) -> tuple[str, int, int]:
        with self._transaction(db):
            token = crud_otp.get_valid_active_token(db, lock=True)
            if token is not None:
                return token.otp_value, self._seconds_until_expiry(token.expires_at), token.version

            raw, expires_in, version = self._force_refresh_otp_in_tx(db, issued_by_user_id=issued_by_user_id)
            return raw, expires_in, version

    def force_refresh_otp(self, db: Session, issued_by_user_id: str | None = None) -> tuple[str, int, int]:
        with self._transaction(db):
            return self._force_refresh_otp_in_tx(db, issued_by_user_id=issued_by_user_id)

    def _force_refresh_otp_in_tx(self, db: Session, issued_by_user_id: str | None = None) -> tuple[str, int, int]:
        # Serialize refresh/create to avoid concurrent active OTP creation.
        db.execute(text("SELECT pg_advisory_xact_lock(:lock_key)"), {"lock_key": self._LOCK_KEY})
        current = crud_otp.get_latest_active_token(db, lock=True)
        version = 1
        if current is not None:
            # Keep OTP history only for tokens that were actually used.
            if current.used_at is None:
                crud_otp.delete_token(db, current)
            else:
                crud_otp.deactivate_token(db, current)
            version = current.version + 1

        raw = self._generate_raw_otp()
        created = crud_otp.create_token(db, raw, issued_by_user_id=issued_by_user_id, version=version)
        return raw, self._seconds_until_expiry(created.expires_at), created.version

    def verify_and_rotate(
        self,
        db: Session,
        user_id: str,
        otp_raw: str,
        enforce_cooldown: bool = True,
    ) -> tuple[bool, str, int | None]:
        now = datetime.now(timezone.utc)

        with self._transaction(db):
            if enforce_cooldown:
                latest_user_verification_stmt = (
                    select(OTPVerification)
                    .where(OTPVerification.user_id == user_id)
                    .order_by(desc(OTPVerification.created_at))
                    .limit(1)
                )
                latest_user_verification = db.execute(latest_user_verification_stmt).scalar_one_or_none()
                if latest_user_verification is not None:
                    verify_time = (
                        latest_user_verification.created_at.replace(tzinfo=timezone.utc)
                        if latest_user_verification.created_at.tzinfo is None
                        else latest_user_verification.created_at
                    )
                    if int((now - verify_time).total_seconds()) < settings.otp_refresh_cooldown_seconds:
                        wait_for = settings.otp_refresh_cooldown_seconds - int((now - verify_time).total_seconds())
                        return False, f"Bạn đã verify gần đây. Vui lòng thử lại sau {wait_for}s.", None

            token = crud_otp.get_valid_active_token(db, lock=True)
            if token is None:
                _, expires_in, _ = self._force_refresh_otp_in_tx(db)
                return False, "OTP hết hạn. Vui lòng lấy OTP mới từ admin.", expires_in

            if not crud_otp.verify_raw_otp(token, otp_raw.strip().upper()):
                return False, "OTP không hợp lệ", None

            crud_otp.consume_token(db, token)

            verification = OTPVerification(user_id=user_id, otp_token_id=token.id)
            db.add(verification)

            _, expires_in, _ = self._force_refresh_otp_in_tx(db)
            return True, "Xác minh thành công. OTP đã được làm mới ngay lập tức.", expires_in


otp_service = OTPService()
