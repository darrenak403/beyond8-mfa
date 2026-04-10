import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import jwt
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from app.core.config import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

SAFE_CHARS = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"

# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------


def create_access_token(subject: str, role: str, session_id: str | None = None) -> str:
    issued_at = datetime.now(timezone.utc)
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    payload: Dict[str, Any] = {
        "sub": subject,
        "role": role,
        "iat": int(issued_at.timestamp()),
        "exp": expire,
    }
    if session_id is not None:
        payload["sid"] = session_id
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def access_token_expires_in_seconds() -> int:
    return max(1, settings.jwt_access_token_expire_minutes * 60)


def create_course_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.course_access_token_expire_days)
    payload: Dict[str, Any] = {
        "sub": subject,
        "role": "course_viewer",
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


# ---------------------------------------------------------------------------
# Password / value hashing helpers
# ---------------------------------------------------------------------------


def hash_value(raw_value: str) -> str:
    return pwd_context.hash(raw_value)


def verify_hash(raw_value: str, hashed_value: str) -> bool:
    try:
        return pwd_context.verify(raw_value, hashed_value)
    except (ValueError, UnknownHashError):
        return False


# ---------------------------------------------------------------------------
# Stateless HMAC OTP helpers
# ---------------------------------------------------------------------------


def _otp_raw_from_digest(digest_hex: str) -> str:
    """
    Map 12 hex nibbles (first 48 bits of HMAC) to safe-character OTP string.
    Format: <PREFIX>-XXXX-XXXX-XXXX  (same style as before)
    """
    # Use first 12 hex chars → 6 bytes → convert each nibble to SAFE_CHARS index
    nibbles = [int(c, 16) for c in digest_hex[:12]]
    # Each nibble is 0-15; SAFE_CHARS has 31 chars — map uniformly
    chars = "".join(SAFE_CHARS[n % len(SAFE_CHARS)] for n in nibbles)
    return f"{settings.key_prefix}-{chars[0:4]}-{chars[4:8]}-{chars[8:12]}"


def generate_otp_for_window(window_id: int) -> str:
    """
    Deterministically generate the OTP for a given HMAC window.
    Same window_id + same jwt_secret_key  →  always the same OTP string.
    No database write needed.
    """
    message = f"otp:{window_id}".encode()
    digest = hmac.new(settings.jwt_secret_key.encode(), message, hashlib.sha256).hexdigest()
    return _otp_raw_from_digest(digest)


def verify_otp_for_window(otp_raw: str, window_id: int) -> bool:
    """Constant-time comparison to avoid timing attacks."""
    expected = generate_otp_for_window(window_id)
    return hmac.compare_digest(
        otp_raw.strip().upper(),
        expected.strip().upper(),
    )
