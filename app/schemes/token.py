"""Authentication token pydantic schemes.

"""

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: EmailStr
    exp: int
