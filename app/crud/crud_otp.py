from datetime import datetime, timedelta, timezone

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_value, verify_hash
from app.models.otp_token import OTPToken


class CRUDOTP:
    def get_latest_active_token(self, db: Session, lock: bool = False) -> OTPToken | None:
        stmt = select(OTPToken).where(OTPToken.is_active.is_(True)).order_by(desc(OTPToken.created_at)).limit(1)
        if lock:
            stmt = stmt.with_for_update()
        return db.execute(stmt).scalar_one_or_none()

    def get_valid_active_token(self, db: Session, lock: bool = False) -> OTPToken | None:
        token = self.get_latest_active_token(db, lock=lock)
        if token is None:
            return None

        now = datetime.now(timezone.utc)
        expires_at = token.expires_at.replace(tzinfo=timezone.utc) if token.expires_at.tzinfo is None else token.expires_at
        if token.used_at is not None or expires_at <= now:
            return None
        return token

    def create_token(self, db: Session, otp_raw: str, issued_by_user_id: str | None, version: int) -> OTPToken:
        now = datetime.now(timezone.utc)
        token = OTPToken(
            otp_value=otp_raw,
            otp_hash=hash_value(otp_raw),
            otp_hint=f"{settings.key_prefix}-{otp_raw[-4:]}",
            issued_by_user_id=issued_by_user_id,
            ttl_seconds=settings.otp_ttl_seconds,
            version=version,
            expires_at=now + timedelta(seconds=settings.otp_ttl_seconds),
        )
        db.add(token)
        db.flush()
        return token

    def consume_token(self, db: Session, token: OTPToken) -> None:
        token.used_at = datetime.now(timezone.utc)
        token.is_active = False
        db.add(token)

    def deactivate_token(self, db: Session, token: OTPToken) -> None:
        token.is_active = False
        db.add(token)

    def delete_token(self, db: Session, token: OTPToken) -> None:
        db.delete(token)

    def verify_raw_otp(self, token: OTPToken, otp_raw: str) -> bool:
        return verify_hash(otp_raw, token.otp_hash)


crud_otp = CRUDOTP()
