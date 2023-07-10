from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.database.models.user import User
from app.schemes.user import UserSignUp, UserUpdate, UserCreate


class CRUDUser(CRUDBase[User, UserSignUp | UserCreate, UserUpdate]):

    async def get_by_email(self, db: Session, *, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    async def set_superuser(self, db: Session, user: User, is_superuser: bool) -> User:
        user.is_superuser = is_superuser
        db.commit()
        db.refresh(user)
        return user

    async def create(self, db: Session, *, obj_in) -> User:
        db_obj = User(
            name=obj_in.name,
            email=obj_in.email,
            password=await get_password_hash(obj_in.password),
            is_superuser=getattr(obj_in, "is_superuser", False),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update_password(self, db: Session, user: User, password: str) -> User:
        user.password = await get_password_hash(password)
        db.commit()
        db.refresh(user)
        return user

    async def authenticate(self, db: Session, email: str, password: str) -> User:
        user = await self.get_by_email(db=db, email=email)
        if not user:
            return None

        if not await verify_password(password, user.password):
            return None

        return user

    async def is_superuser(self, user: User) -> bool:
        return user.is_superuser


crud_user = CRUDUser(User)
