from httpx import AsyncClient

from app.core import config
from app.database.models.user import User
from app.schemes.token import AccsessTokenData
from app.utils.token import decode_jwt
from app.tests.utils.utils import random_lower_string, random_email


async def test_get_access_token(client: AsyncClient, first_superuser: User) -> None:
    login_data = {
        "username": config.FIRST_SUPERUSER_EMAIL,
        "password": config.FIRST_SUPERUSER_PASSWORD,
        "scope": None,
        "client_id": None,
        "client_secret": None,
    }
    r = await client.post("/signin", data=login_data)
    response_json = r.json()
    assert r.status_code == 200
    assert "access_token" in response_json
    assert response_json["access_token"]


async def test_use_access_token(client: AsyncClient, superuser_token_headers: dict[str: str]) -> None:
    r = await client.post("/test-token", headers=await superuser_token_headers)
    assert r.status_code == 200
    assert "email" in r.json()


async def test_refresh_token(client: AsyncClient, superuser_access_token: dict[str: str]) -> None:
    token_data: AccsessTokenData = await decode_jwt(superuser_access_token, AccsessTokenData)
    r = await client.post(f"/refresh?refresh_token={token_data.refresh_token}")
    response_json = r.json()
    assert r.status_code == 200
    assert "access_token" in response_json
    assert response_json["access_token"]


async def test_signup(client: AsyncClient):
    name = await random_lower_string()
    email = await random_email()
    password = await random_lower_string()
    sign_up_data = {
        "name": name,
        "email": email,
        "password": password,
        "password_repeat": password
    }
    r = await client.post("/signup", json=sign_up_data)
    response_json = r.json()
    assert r.status_code == 200
    assert "name" in response_json
    assert response_json["name"] == name
    assert "email" in response_json
    assert response_json["email"] == email
    assert "password" in response_json
