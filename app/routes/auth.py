from datetime import datetime

from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import config
from app.crud.user import crud_user
from app.database.session import get_db
from app.schemes.user import UserBase, UserSignUp
from app.schemes.token import TokenResponce, RefreshTokenData
from app.utils.HTTP_errors import HTTP_400_BAD_REQUEST
from app.utils.token import decode_jwt, create_new_jwt


router = APIRouter(tags=["auth"])
jwt_auth_path = config.JWT_AUTH_PATH

@router.post(jwt_auth_path, response_model=TokenResponce)
async def signin_jwt(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponce:
    user = await crud_user.authenticate(
        db,
        email=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTP_400_BAD_REQUEST("Invalid email or password")
    return await create_new_jwt({"email": user.email,"id": user.id})


@router.post("/refresh")
async def refresh(refresh_token: str, db: Session = Depends(get_db)):
    token_data: RefreshTokenData = await decode_jwt(refresh_token, RefreshTokenData)
    token_expired = datetime.utcfromtimestamp(token_data.exp) < datetime.utcnow()
    if token_expired:
        return HTTP_400_BAD_REQUEST("Token is expired")
    user = await crud_user.get(db, id=token_data.id)
    if not user:
        return HTTP_400_BAD_REQUEST("Invalid user")
    return await create_new_jwt({"email": user.email, "id": user.id})


@router.post("/signup", response_model=UserBase)
async def user_signup(*, user_in: UserSignUp, db: Session = Depends(get_db)) -> UserBase:
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user is not None:
        raise HTTP_400_BAD_REQUEST("User already exists")
    return await crud_user.create(db, obj_in=user_in)
