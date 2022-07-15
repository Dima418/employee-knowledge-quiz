from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.core import config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{config.JWT_AUTH_PATH}")

async def create_jwt(token_data: dict, refresh: bool = False) -> str:
    if refresh:
        expires_delta = timedelta(minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES)
    else:
        expires_delta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta

    to_encode = token_data.copy()
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ENCODING_ALGORITHM)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
