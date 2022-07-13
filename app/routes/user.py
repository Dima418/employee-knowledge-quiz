from fastapi import APIRouter, Depends
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from app.crud.user import crud_user
from app.database.base import User
from app.database.session import get_db
from app.schemes import UserBase, UserUpdate
from app.utils.user import get_current_user


router = APIRouter(tags=["user"])

@router.get("/users/", response_model=list[UserBase])
async def all_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user)
) -> list[UserBase]:
    """
    Retrieve users.
    """
    users = await crud_user.get_multi(db, skip=skip, limit=limit)
    return parse_obj_as(list[UserBase], users)


@router.put("/update/me", response_model=UserBase)
async def update_user_me(
    *,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserBase:
    """
    Update own user.
    """
    user = await crud_user.update(db, old_obj=current_user, new_obj=user_in)
    return UserBase.from_orm(user)


@router.delete("/user/{user_id}", response_model=UserBase)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete user with specific id.
    """
    user = await crud_user.delete(db, id=user_id)
    return user
