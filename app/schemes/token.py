from pydantic import BaseModel, EmailStr


class TokenResponce(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: EmailStr
    id: int


class AccsessTokenData(TokenData):
    refresh_token: str
    exp: int


class RefreshTokenData(TokenData):
    exp: int
