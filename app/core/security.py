"""Authentication module.

Contains the authentication logic for the application.

"""

from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.core import config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{config.JWT_AUTH_PATH}")

async def create_access_token(
    subject: dict,
    expires_delta: timedelta | None = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
) -> str:
    """Create an access token for the given subject.

    Args:
        subject (dict): The subject of the token.
        expires_delta (timedelta, optional): Time delta for token expiration.
            Defaults to timedelta (minutes) for ``ACCESS_TOKEN_EXPIRE_MINUTES`` from config file.

    Returns:
        (str): The encoded access token.
    """
    to_encode = subject.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ENCODING_ALGORITHM)
    return encoded_jwt


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        (bool): Whether the password is correct.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str) -> str:
    """Get the hashed password for the given password.

    Args:
        password (str): The password to hash.

    Returns:
        (str): The hashed password.
    """
    return pwd_context.hash(password)
