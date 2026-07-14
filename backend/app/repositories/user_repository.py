from sqlalchemy.orm import Session
from app.models.user import User
from sqlalchemy import select

class UserRepository:
    @staticmethod
    def get_by_email(db: Session,email: str,) -> User | None:
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def create(db: Session,user: User,) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user