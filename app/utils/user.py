from fastapi import Depends
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import config
from app.core.security import reusable_oauth2
from app.crud.user import crud_user
from app.database.session import get_db
from app.database.models.user import User
from app.schemes.token import TokenData
from app.utils.HTTP_errors import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ENCODING_ALGORITHM])
        token_data = TokenData(**payload)

        if token_data.sub is None:
            raise HTTP_401_UNAUTHORIZED
    except (jwt.JWTError, ValidationError):
        raise HTTP_403_FORBIDDEN

    user = await crud_user.get_by_email(db, email=token_data.sub)

    if user is None:
        raise HTTP_404_NOT_FOUND

    return user
