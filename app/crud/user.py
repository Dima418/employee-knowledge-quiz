"""CRUD class for ``User`` model.

"""

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.database.models.user import User
from app.schemes.user import UserSignUp, UserUpdate
from app.utils.HTTP_errors import HTTP_400_BAD_REQUEST


class CRUDUser(CRUDBase[User, UserSignUp, UserUpdate]):
    """Class for CRUD operations on ``User`` model.

    Args:
        CRUDBase: The CRUD base class.
    """

    async def get_by_email(self, db: Session, *, email: str) -> User | None:
        """Get user by email.

        Args:
            db (Session): The database session.
            email (str): The email.

        Returns:
            (User, optional): The user or None.
        """
        return db.query(User).filter(User.email == email).first()

    async def create(self, db: Session, *, obj_in: UserSignUp) -> User:
        """Create new user.

        Args:
            db (Session): The database session.
            obj_in (UserSignUp): The user sign up data.

        Returns:
            (User): The created user.
        """
        db_obj = User(
            name=obj_in.name,
            email=obj_in.email,
            password=await get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def authenticate(self, db: Session, email: str, password: str) -> User:
        """Authenticate user.

        Args:
            db (Session): The database session.
            email (str): The email.
            password (str): The password.

        Raises:
            HTTP_400_BAD_REQUEST: If user is not found or password is incorrect.

        Returns:
            (User): The user.
        """
        user = await self.get_by_email(db=db, email=email)
        if user is None:
            raise HTTP_400_BAD_REQUEST("Invalid email or password")

        if not await verify_password(password, user.password):
            raise HTTP_400_BAD_REQUEST("Invalid email or password")

        return user

    def is_superuser(self, user: User) -> bool:
        """Check if user is superuser.

        Args:
            user (User): The user.

        Returns:
            (bool): True if user is superuser.
        """
        return user.is_superuser


crud_user = CRUDUser(User)
