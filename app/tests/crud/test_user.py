import pytest
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.user import crud_user
from app.core.security import verify_password
from app.schemes.user import UserUpdate, UserCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_create_normal_user(db: Session) -> None:
    user = await create_random_user(db=db)
    assert hasattr(user, "email")
    assert user.email
    assert hasattr(user, "password")
    assert user.password


@pytest.mark.anyio
async def test_create_superuser(db: Session) -> None:
    user = await create_random_user(db=db, is_superuser=True)
    assert hasattr(user, "email")
    assert user.email
    assert hasattr(user, "password")
    assert user.password
    assert user.is_superuser


@pytest.mark.anyio
async def test_authenticate_user(db: Session) -> None:
    email = await random_email()
    password = await random_lower_string()
    user = await crud_user.create(
        db=db,
        obj_in=UserCreate(
            name=await random_lower_string(),
            email=email,
            password=password,
            is_superuser=False
        )
    )
    authenticated_user = await crud_user.authenticate(db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


@pytest.mark.anyio
async def test_not_authenticate_user(db: Session) -> None:
    email = "unique." + await random_email()
    password = await random_lower_string()
    user = await crud_user.authenticate(db, email=email, password=password)
    assert not user


@pytest.mark.anyio
async def test_check_if_user_is_superuser(db: Session) -> None:
    user = await create_random_user(db=db, is_superuser=True)
    is_superuser = await crud_user.is_superuser(user)
    assert is_superuser


@pytest.mark.anyio
async def test_check_if_normal_user_is_superuser(db: Session) -> None:
    user = await create_random_user(db=db)
    is_superuser = await crud_user.is_superuser(user)
    assert not is_superuser


@pytest.mark.anyio
async def test_get_user(db: Session) -> None:
    user = await create_random_user(db=db)
    user_2 = await crud_user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


@pytest.mark.anyio
async def test_update_user_email(db: Session) -> None:
    user = await create_random_user(db=db)
    new_name = await random_lower_string()
    new_email = await random_email()
    user_in_update = UserUpdate(name=new_name, email=new_email)
    await crud_user.update(db, old_obj=user, new_obj=user_in_update)
    user_2 = await crud_user.get(db, id=user.id)
    assert user_2
    assert user_2.id == user.id
    assert user_2.name == new_name
    assert user_2.email == new_email


@pytest.mark.anyio
async def test_update_user_password(db: Session) -> None:
    user = await create_random_user(db=db)
    new_password = await random_lower_string()
    await crud_user.update_password(db, user, new_password)
    user_2 = await crud_user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert await verify_password(new_password, user_2.password)


@pytest.mark.anyio
async def test_delete_user(db: Session) -> None:
    user = await create_random_user(db=db)
    deleted_user = await crud_user.delete(db, id=user.id)
    assert not await crud_user.get(db, id=deleted_user.id)
