from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from app.crud.user import crud_user
from app.database.session import get_db
from app.schemas.user import UserSchema, UserSignUpSchema
from app.utils.user import get_current_user


router = APIRouter(tags=["user"])

@router.get("/users/", response_model=list[UserSchema])
async def all_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    current_user: UserSchema = Depends(get_current_user)
) -> list[UserSchema]:
    """
    Retrieve users.
    """
    users = await crud_user.get_multi(db, skip=skip, limit=limit)
    return parse_obj_as(list[UserSchema], users)


@router.post("/signup/", response_model=UserSchema)
async def user_signup(
    *,
    user_in: UserSignUpSchema,
    db: Session = Depends(get_db),
):
    """
    Create new user.
    """
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )
    user = await crud_user.create(db, obj_in=user_in)
    return user


@router.delete("/user/{user_id}", response_model=UserSchema)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    """
    Delete user with specific id.
    """
    user = await crud_user.delete(db, id=user_id)
    return user
