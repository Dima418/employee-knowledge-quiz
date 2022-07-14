from jose import jwt
from pydantic import ValidationError

from app.core import config
from app.core.security import create_jwt
from app.schemes.token import TokenResponce
from app.utils.HTTP_errors import HTTP_403_FORBIDDEN


async def decode_jwt(
    token: str,
    decode_model: type,
    secret: str = config.SECRET_KEY,
    algorithms: str = [config.ENCODING_ALGORITHM]
) -> dict:
    try:
        payload = jwt.decode(token, secret, algorithms=algorithms)
        token_data = decode_model(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTP_403_FORBIDDEN("Invalid token")
    return token_data


async def create_new_jwt(token_data) -> TokenResponce:
    refresh_token= await create_jwt(token_data, refresh=True)
    token_data.update({"refresh_token": refresh_token})
    access_token= await create_jwt(token_data)
    return TokenResponce(access_token=access_token)
