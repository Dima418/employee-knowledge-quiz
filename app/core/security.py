from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth
from jose import jwt
from passlib.context import CryptContext

from app.core import config


# OAuth for Google

def _setup_oauth() -> OAuth:
    if config.GOOGLE_CLIENT_ID is None or config.GOOGLE_CLIENT_SECRET is None:
        raise BaseException("Missing env variables")

    config_data = {
        "GOOGLE_CLIENT_ID": config.GOOGLE_CLIENT_ID,
        "GOOGLE_CLIENT_SECRET": config.GOOGLE_CLIENT_SECRET
    }
    starlette_config = Config(environ=config_data)

    oauth = OAuth(starlette_config)
    oauth.register(
        name='google',
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'},
    )
    return oauth

oauth: OAuth = _setup_oauth()


# Authentication with JWT

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{config.JWT_AUTH_PATH}")

async def create_access_token(
    subject: dict,
    expires_delta: timedelta | None = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
) -> str:
    to_encode = subject.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ENCODING_ALGORITHM)
    return encoded_jwt


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
