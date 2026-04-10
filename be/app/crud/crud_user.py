from sqlalchemy import func, select
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

    def get_all(
        self,
        db: Session,
        offset: int = 0,
        limit: int = 100,
        search: str | None = None,
    ) -> tuple[list[User], int]:
        stmt = select(User)
        total_stmt = select(func.count(User.id))

        normalized_search = search.strip().lower() if search else ""
        if normalized_search:
            search_filter = func.lower(User.email).contains(normalized_search, autoescape=True)
            stmt = stmt.where(search_filter)
            total_stmt = total_stmt.where(search_filter)

        stmt = stmt.order_by(User.created_at.desc(), User.id.desc()).offset(offset).limit(limit)

        users = list(db.execute(stmt).scalars().all())
        total = int(db.execute(total_stmt).scalar_one() or 0)
        return users, total

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
