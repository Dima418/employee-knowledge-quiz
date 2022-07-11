from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import config
from app.core.security import create_access_token
from app.crud.user import crud_user
from app.database.session import get_db
from app.schemes.token import Token
from app.schemes.user import UserBase, UserSignUp
from app.utils.HTTP_errors import HTTP_400_BAD_REQUEST


router = APIRouter(tags=["auth"])
jwt_auth_path = config.JWT_AUTH_PATH

@router.post(jwt_auth_path, response_model=Token)
async def signin_jwt(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = await crud_user.authenticate(
        db,
        email=form_data.username,
        password=form_data.password
    )

    if user is None:
        raise HTTP_400_BAD_REQUEST

    user_data = {"sub": user.email}
    access_token = await create_access_token(user_data)

    return Token(access_token=access_token)


@router.post("/signup", response_model=UserBase)
async def user_signup(*, user_in: UserSignUp, db: Session = Depends(get_db)) -> UserBase:
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user is not None:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = await crud_user.create(db, obj_in=user_in)
    return user
