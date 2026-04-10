from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.crud import crud_user
from app.models.user import User


class AuthService:
    def signin(self, db: Session, email: str) -> tuple[str, User]:
        normalized_email = email.lower().strip()

        if normalized_email == settings.seed_admin_email.lower().strip():
            user = crud_user.get_or_create(db, normalized_email, "admin")
            token = create_access_token(subject=user.id, role=user.role_name)
            return token, user

        # Preserve existing role (e.g. admin). Only create a new account as "user" if missing.
        user = crud_user.get_by_email(db, normalized_email)
        if user is None:
            user = crud_user.get_or_create(db, normalized_email, "user")

        token = create_access_token(subject=user.id, role=user.role_name)
        return token, user

    def get_all_users(
        self,
        db: Session,
        offset: int = 0,
        limit: int = 100,
        search: str | None = None,
    ) -> tuple[list[User], int]:
        return crud_user.get_all(db, offset=offset, limit=limit, search=search)


auth_service = AuthService()
