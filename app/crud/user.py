from sqlalchemy.orm import Session

from app.database.models.user import User
from app.schemas.user import UserSignUp


class UserCRUD():
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: UserSignUp) -> User:
            db_obj = User(
                name=obj_in.name,
                email=obj_in.email,
                password=obj_in.password,
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

    def get_by_email(self, db: Session, *, email: str) -> User:
            return db.query(User).filter(User.email == email).first()

    def get_by_id(self, db: Session, *, id: int) -> User:
            return db.query(User).filter(User.id == id).first()

    def delete(self, db: Session, *, id: int) -> User:
            obj = db.query(User).get(id)
            db.delete(obj)
            db.commit()
            return obj

user = UserCRUD()
