from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.user import user as crud_user
from app.database import session
from app.schemas.user import User, UserSignUp, UserSignIn


router = APIRouter(tags=["user"])

@router.get("/users/", response_model=list[User])
def all_users(
    db: Session = Depends(session.get_db),
    skip: int = 0,
    limit: int = 10
) -> list[User]:
    """
    Retrieve users.
    """
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/signup/", response_model=User)
def user_signup(
    *,
    user_in: UserSignUp,
    db: Session = Depends(session.get_db),
):
    """
    Create new user.
    """
    user = crud_user.create(db, obj_in=user_in)
    return user


@router.post("/signin/", response_model=User)
def user_signin(
    *,
    user_in: UserSignIn,
    db: Session = Depends(session.get_db),
):
    """
    Create new user.
    """
    user = crud_user.get_by_email(db, email=user_in.email)
    return user


@router.delete("/user/{user_id}", response_model=User)
def delete_user(
    user_id: int,
    db: Session = Depends(session.get_db),
):
    """
    Delete user with specific id.
    """
    user = crud_user.delete(db, id=user_id)
    return user
