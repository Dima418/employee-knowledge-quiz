from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import config
from app.core.security import create_access_token
from app.crud.user import crud_user
from app.database.session import get_db
from app.schemas.user import UserSignInSchema
from app.schemas.token import Token


router = APIRouter(tags=["signin"])

token_url = config.ACCESS_TOKEN_URL


@router.post(token_url, response_model=Token)
async def generate_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud_user.authenticate(
        db,
        email=form_data.username,
        password=form_data.password
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    user_data = UserSignInSchema.from_orm(user).dict()
    access_token = await create_access_token(user_data, access_token_expires)

    return Token(access_token=access_token)
