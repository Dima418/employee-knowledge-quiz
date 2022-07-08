from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.database.models.user import User
from app.schemas.user import UserSignUpSchema


class UserCRUD():
    async def get(self, db: Session, id: int) -> User | None:
        return db.query(User).filter(self.model.id == id).first()

    async def get_by_email(self, db: Session, *, email: str) -> User:
            return db.query(User).filter(User.email == email).first()

    async def get_by_id(self, db: Session, *, id: int) -> User:
            return db.query(User).filter(User.id == id).first()

    async def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    async def create(self, db: Session, *, obj_in: UserSignUpSchema) -> User:
            db_obj = User(
                name=obj_in.name,
                email=obj_in.email,
                password=await get_password_hash(obj_in.password),
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

    async def delete(self, db: Session, *, id: int) -> User:
            obj = db.query(User).get(id)
            db.delete(obj)
            db.commit()
            return obj

    async def authenticate(self, db: Session, email: str, password: str) -> User:
        user = await self.get_by_email(db=db, email=email)
        if user is None:
                raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
        if not await verify_password(password, user.password):
                raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
        return user

crud_user = UserCRUD()
