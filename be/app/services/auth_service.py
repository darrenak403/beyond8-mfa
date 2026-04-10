from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid

from app.core.config import settings
from app.core.security import access_token_expires_in_seconds, create_access_token
from app.crud import crud_user
from app.models.user import User
from datetime import datetime, timedelta, timezone


class AuthService:
    def signin(self, db: Session, email: str) -> tuple[str, str, int, User]:
        normalized_email = email.lower().strip()

        if normalized_email == settings.seed_admin_email.lower().strip():
            user = crud_user.get_or_create(db, normalized_email, "admin")
        else:
            # Preserve existing role (e.g. admin). Only create a new account as "user" if missing.
            user = crud_user.get_by_email(db, normalized_email)
            if user is None:
                user = crud_user.get_or_create(db, normalized_email, "user")

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tài khoản đã bị khóa. Vui lòng liên hệ quản trị viên.",
            )

        refresh_token = f"{uuid.uuid4()}{uuid.uuid4()}"
        crud_user.rotate_refresh_token(db, user=user, refresh_token=refresh_token)
        token = create_access_token(subject=user.id, role=user.role_name)
        return token, refresh_token, access_token_expires_in_seconds(), user

    def refresh_access_token(self, db: Session, refresh_token: str) -> tuple[str, str, int, User]:
        user = crud_user.get_by_refresh_token(db, refresh_token)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token không hợp lệ",
            )

        if user.refresh_token_updated_at is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token đã hết hạn",
            )

        updated_at = user.refresh_token_updated_at
        if updated_at.tzinfo is None:
            updated_at = updated_at.replace(tzinfo=timezone.utc)
        expires_at = updated_at + timedelta(days=settings.refresh_token_expire_days)
        if datetime.now(timezone.utc) >= expires_at:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token đã hết hạn",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tài khoản đã bị khóa. Vui lòng liên hệ quản trị viên.",
            )

        new_refresh_token = f"{uuid.uuid4()}{uuid.uuid4()}"
        crud_user.rotate_refresh_token(db, user=user, refresh_token=new_refresh_token)
        access_token = create_access_token(subject=user.id, role=user.role_name)
        return access_token, new_refresh_token, access_token_expires_in_seconds(), user

    def get_all_users(
        self,
        db: Session,
        offset: int = 0,
        limit: int = 100,
        search: str | None = None,
    ) -> tuple[list[User], int]:
        return crud_user.get_all(db, offset=offset, limit=limit, search=search)

    def block_user(
        self,
        db: Session,
        *,
        user_id: str,
        admin_user_id: str,
        reason: str | None = None,
    ) -> User:
        user = crud_user.get_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng")

        if user.role_name == "admin":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể khóa tài khoản admin")

        if user.id == admin_user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể tự khóa chính mình")

        updated = crud_user.set_block_status(
            db,
            user_id=user.id,
            is_active=False,
            blocked_by_user_id=admin_user_id,
            blocked_reason=reason,
        )
        if updated is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng")
        return updated

    def unblock_user(self, db: Session, *, user_id: str) -> User:
        user = crud_user.get_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng")

        updated = crud_user.set_block_status(
            db,
            user_id=user.id,
            is_active=True,
            blocked_by_user_id=None,
        )
        if updated is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng")
        return updated


auth_service = AuthService()
