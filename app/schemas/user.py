from datetime import datetime
from pydantic import BaseModel, EmailStr, validator, root_validator


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    is_superuser: bool = False
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class UserSignUp(BaseModel):
    name: str
    email: EmailStr
    password: str
    password_repeat: str

    class Config:
        orm_mode = True

    @validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        return password

    @root_validator
    def validate_passwords_match(cls, values):  
        pw1, pw2 = values.get("password"), values.get("password_repeat")
        if pw1 != pw2:
            raise ValueError("Passwords don't match")
        return values


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
