from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.user import crud_user
from app.core.security import verify_password
from app.database.models.user import User
from app.schemes.user import UserUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_email, random_lower_string


async def test_create_normal_user(new_normal_user: User) -> None:
    assert hasattr(new_normal_user, "email")
    assert new_normal_user.email
    assert hasattr(new_normal_user, "password")
    assert new_normal_user.password
    assert not new_normal_user.is_superuser


async def test_create_superuser(new_superuser: User) -> None:
    assert hasattr(new_superuser, "email")
    assert new_superuser.email
    assert hasattr(new_superuser, "password")
    assert new_superuser.password
    assert new_superuser.is_superuser


async def test_authenticate_user(db: Session) -> None:
    email = await random_email()
    password = await random_lower_string()
    user = await create_random_user(db, email, password)
    authenticated_user = await crud_user.authenticate(db, email, password)
    assert authenticated_user
    assert user.email == authenticated_user.email


async def test_not_authenticate_user(db: Session) -> None:
    email = "unique." + await random_email()
    password = await random_lower_string()
    user = await crud_user.authenticate(db, email, password)
    assert not user


async def test_check_if_user_is_superuser(new_superuser: User) -> None:
    assert await crud_user.is_superuser(new_superuser)


async def test_check_if_normal_user_is_superuser(new_normal_user: User) -> None:
    assert not await crud_user.is_superuser(new_normal_user)


async def test_get_user(db: Session, new_normal_user: User) -> None:
    same_user = await crud_user.get(db, id=new_normal_user.id)
    assert same_user
    assert new_normal_user.email == same_user.email
    assert jsonable_encoder(new_normal_user) == jsonable_encoder(same_user)


async def test_update_user_name_and_email(db: Session, new_normal_user: User) -> None:
    new_name = await random_lower_string()
    new_email = await random_email()
    user_in_update = UserUpdate(name=new_name, email=new_email)
    await crud_user.update(db, old_obj=new_normal_user, new_obj=user_in_update)
    same_user = await crud_user.get(db, id=new_normal_user.id)
    assert same_user
    assert same_user.id == new_normal_user.id
    assert same_user.name == new_name
    assert same_user.email == new_email


async def test_update_user_password(db: Session, new_normal_user: User) -> None:
    new_password = await random_lower_string()
    await crud_user.update_password(db, new_normal_user, new_password)
    user_2 = await crud_user.get(db, id=new_normal_user.id)
    assert user_2
    assert new_normal_user.email == user_2.email
    assert await verify_password(new_password, user_2.password)


async def test_delete_user(db: Session, new_normal_user: User) -> None:
    deleted_user = await crud_user.delete(db, id=new_normal_user.id)
    assert not await crud_user.get(db, id=deleted_user.id)
