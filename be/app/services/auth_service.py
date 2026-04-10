from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.crud import crud_user
from app.models.user import User


class AuthService:
    def signin(self, db: Session, email: str) -> tuple[str, User]:
        normalized_email = email.lower().strip()

        # Open signin/login: create user with default role if not exists.
        user = crud_user.get_or_create(db, normalized_email, "user")

        token = create_access_token(subject=user.id, role=user.role_name)
        return token, user


auth_service = AuthService()
