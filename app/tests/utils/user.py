from sqlalchemy.orm import Session
from httpx import AsyncClient

from app.crud.user import crud_user
from app.database.models.user import User
from app.schemes.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


async def create_random_user(db: Session, email: str = None, password: str = None, is_superuser: bool = False) -> User:
    return await crud_user.create(
        db=db,
        obj_in=UserCreate(
            name=await random_lower_string(),
            email=email or await random_email(),
            password=password or await random_lower_string(),
            is_superuser=is_superuser
        )
    )


async def get_access_token(client: AsyncClient, email: str, password: str) -> str:
    login_data = {
        "username": email,
        "password": password,
        "scope": None,
        "client_id": None,
        "client_secret": None,
    }
    r = await client.post("/signin", data=login_data)
    return r.json()["access_token"]


async def get_user_authentication_headers(client: AsyncClient, email: str, password: str) -> dict[str: str]:
    return {"Authorization": f"Bearer {await get_access_token(client, email, password)}"}
