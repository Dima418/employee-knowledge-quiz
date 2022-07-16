from sqlalchemy.orm import Session

from app.crud.user import crud_user
from app.database.models.user import User
from app.schemes.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


async def create_random_user(db: Session, is_superuser: bool = False) -> User:
    return await crud_user.create(
        db=db,
        obj_in=UserCreate(
            name=await random_lower_string(),
            email=await random_email(),
            password=await random_lower_string(),
            is_superuser=is_superuser
        )
    )
