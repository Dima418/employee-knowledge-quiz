from datetime import datetime
from pydantic import BaseModel, EmailStr, root_validator


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

    @root_validator(pre=True)
    def validate_password(cls, values):
        password = values.get("password")
        if password == "":
            raise ValueError('Password is required')
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        return values

    @root_validator
    def validate_passwords_match(cls, values):
        pw1, pw2 = values.get('password'), values.get('password_repeat')
        if pw1 is not None and pw2 is not None and pw1 is not pw2:
            raise ValueError("Passwords don't match")
        return values


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

    @root_validator(pre=True)
    def validate_password(cls, values):
        password = values.get("password")
        if password == "":
            raise ValueError('Password is required')
        return values
