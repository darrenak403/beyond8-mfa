from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import create_access_token, generate_otp_for_user_window
from app.crud import crud_otp, crud_user
from app.models.user import User


class AuthService:
    def signup(self, db: Session, email: str) -> bool:
        normalized_email = email.lower().strip()

        if normalized_email == settings.seed_admin_email.lower().strip():
            crud_user.get_or_create(db, normalized_email, "admin")
        else:
            user = crud_user.get_by_email(db, normalized_email)
            if user is None:
                crud_user.get_or_create(db, normalized_email, "user")

        return True

    def signin(self, db: Session, email: str) -> tuple[str, User]:
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

        token = create_access_token(subject=user.id, role=user.role_name, email=user.email)
        return token, user

    def get_all_users(
        self,
        db: Session,
        offset: int = 0,
        limit: int = 100,
        search: str | None = None,
    ) -> tuple[list[User], int]:
        return crud_user.get_all(db, offset=offset, limit=limit, search=search)

    def get_user_by_id(self, db: Session, *, user_id: str) -> User:
        user = crud_user.get_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng")
        return user

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
        revoked_user = crud_user.revoke_course_access(db, user_id=user.id)
        if revoked_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng")
        return revoked_user

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

    def revoke_course_access(self, db: Session, *, user_id: str) -> User:
        user = crud_user.get_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng")

        updated = crud_user.revoke_course_access(db, user_id=user.id)
        if updated is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng")
        return updated

    def clear_verified_otp_key(self, db: Session, *, user_id: str) -> User:
        user = crud_user.get_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng")

        updated = crud_user.clear_verified_otp_key(db, user_id=user.id)
        if updated is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng")

        # Rotate OTP immediately so the previous key is invalid and a fresh
        # key is available in last_generated_otp right after clear.
        try:
            new_rotate_count = crud_otp.increment_user_rotate_count(db, user_id=user.id)
            new_otp = generate_otp_for_user_window(
                user_id=user.id,
                otp_rotate_count=new_rotate_count,
            )
            crud_otp.save_last_generated_otp(db, user_id=user.id, otp_value=new_otp)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy người dùng",
            ) from exc
        return updated

    def delete_user(
        self,
        db: Session,
        *,
        user_id: str,
        admin_user_id: str,
    ) -> None:
        user = crud_user.get_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng")

        if user.role_name == "admin":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể xóa tài khoản admin")

        if user.id == admin_user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể tự xóa chính mình")

        deleted = crud_user.hard_delete(db, user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy người dùng")


auth_service = AuthService()
