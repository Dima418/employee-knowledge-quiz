from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.user import crud_user
from app.database.models.user import User
from app.database.session import get_db
from app.schemes.user import UserBase, UserUpdate
from app.utils.user import get_current_user, get_current_superuser
from app.utils.HTTP_errors import HTTP_404_NOT_FOUND


router = APIRouter(tags=["user"])

@router.get("/users/", response_model=list[UserBase])
async def all_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user)
) -> list[UserBase]:
    return await crud_user.get_multi(db, skip=skip, limit=limit)


@router.patch("/update/me", response_model=UserBase)
async def update_user_me(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserBase:
    return await crud_user.update(db, old_obj=current_user, new_obj=user_in)


@router.patch("/update/{user_id}")
async def update_superuser_status(
    user_id: int,
    *,
    is_superuser: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
) -> UserBase:
    user = await crud_user.get(db, id=user_id)
    if not user:
        raise HTTP_404_NOT_FOUND("User not found")
    return await crud_user.set_superuser(db, user, is_superuser)


@router.delete("/user/{user_id}", response_model=UserBase)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    return await crud_user.delete(db, id=user_id)
