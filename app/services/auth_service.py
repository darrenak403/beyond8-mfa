from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.crud import crud_user
from app.models.user import User


class AuthService:
    def signin(self, db: Session, email: str) -> tuple[str, User]:
        normalized_email = email.lower().strip()

        user = crud_user.get_by_email(db, normalized_email)
        if user is None or user.role_name != "admin":
            raise PermissionError("Email không có quyền quản trị")

        token = create_access_token(subject=user.id, role=user.role_name)
        return token, user


auth_service = AuthService()
