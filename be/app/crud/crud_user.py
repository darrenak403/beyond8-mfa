from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.crud_role import crud_role
from app.models.user import User


class CRUDUser:
    def get_by_id(self, db: Session, user_id: str) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return db.execute(stmt).scalar_one_or_none()

    def get_by_email(self, db: Session, email: str) -> User | None:
        stmt = select(User).where(User.email == email.lower())
        return db.execute(stmt).scalar_one_or_none()

    def get_or_create(self, db: Session, email: str, role_name: str) -> User:
        role = crud_role.get_by_name(db, role_name)
        if role is None:
            raise ValueError(f"Role '{role_name}' does not exist")

        user = self.get_by_email(db, email)
        if user is not None:
            if user.role_id != role.id:
                user.role_id = role.id
                db.add(user)
                db.commit()
                db.refresh(user)
            return user

        user = User(email=email.lower(), role_id=role.id)
        db.add(user)
        try:
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            db.rollback()
            existing = self.get_by_email(db, email)
            if existing is None:
                raise
            return existing


crud_user = CRUDUser()
