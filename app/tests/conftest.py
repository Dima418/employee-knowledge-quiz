from typing import Any, AsyncGenerator, Generator

import pytest

from fastapi import FastAPI
from httpx import AsyncClient

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import get_application
from app.core import config
from app.database.base_class import Base
from app.database.models.user import User
from app.database.models.quiz import (
    Quiz,
    Question,
    Category,
    Answer,
    QuizResult
)
from app.database.session import get_db
from app.tests.utils.user import (
    create_random_user,
    get_user_authentication_headers,
    get_access_token
)
from app.tests.utils.quiz import (
    create_random_quiz,
    create_random_question,
    create_random_category,
    create_random_answer,
    create_quiz_result,
    get_nonexistent_quiz,
    get_nonexistent_question,
    get_nonexistent_category,
    get_nonexistent_answer
)
from app.tests.utils.utils import (
    random_email,
    random_lower_string
)


@pytest.fixture()
def db() -> Generator:
    engine = create_engine(config.TEST_DB_DEFAULT)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        _db = TestingSessionLocal()
        yield _db
    finally:
        _db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def override_get_db(db: Generator) -> AsyncGenerator:
    async def _override_get_db():
        yield db

    return _override_get_db


@pytest.fixture()
def app(override_get_db: AsyncGenerator) -> FastAPI:
    app = get_application()
    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac


@pytest.fixture()
async def first_superuser(db: Session) -> User:
    return await create_random_user(
        db,
        config.FIRST_SUPERUSER_EMAIL,
        config.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True
    )


@pytest.fixture()
async def new_superuser(db: Session) -> User:
    return await create_random_user(db, is_superuser=True)


@pytest.fixture()
async def superuser_access_token(client: TestClient, db: Session) -> str:
    email = await random_email()
    password = await random_lower_string()
    await create_random_user(db, email, password, is_superuser=True)
    return await get_access_token(client, email, password)


@pytest.fixture()
async def superuser_token_headers(client: TestClient, db: Session) -> dict[str: str]:
    email = await random_email()
    password = await random_lower_string()
    await create_random_user(db, email, password, is_superuser=True)
    return get_user_authentication_headers(client, email, password)


@pytest.fixture()
async def new_normal_user(db: Session) -> User:
    return await create_random_user(db)


@pytest.fixture()
async def normal_user_token_headers(client: TestClient, db: Session) -> dict[str: str]:
    email = await random_email()
    password = await random_lower_string()
    await create_random_user(db, email, password)
    return get_user_authentication_headers(client, email, password)


@pytest.fixture()
async def new_active_quiz(db: Session) -> Quiz:
    return await create_random_quiz(db, is_active=True)


@pytest.fixture()
async def new_inactive_quiz(db: Session) -> Quiz:
    return await create_random_quiz(db, is_active=False)


@pytest.fixture()
async def nonexistent_quiz() -> Quiz:
    return await get_nonexistent_quiz()


@pytest.fixture()
async def new_question(db: Session, new_active_quiz: Quiz) -> Question:
    return await create_random_question(db, new_active_quiz.id)


@pytest.fixture()
async def nonexistent_question() -> Question:
    return await get_nonexistent_question()


@pytest.fixture()
async def new_category(db: Session) -> Category:
    return await create_random_category(db)


@pytest.fixture()
async def nonexistent_category() -> Category:
    return await get_nonexistent_category()


@pytest.fixture()
async def new_correct_answer(db: Session, new_question: Question) -> Answer:
    return await create_random_answer(db, new_question.id, is_correct=True)


@pytest.fixture()
async def new_incorrect_answer(db: Session, new_question: Question) -> Answer:
    return await create_random_answer(db, new_question.id, is_correct=False)


@pytest.fixture()
async def nonexistent_answer() -> Answer:
    return await get_nonexistent_answer()


@pytest.fixture()
async def new_quiz_result(db: Session, new_normal_user: User, new_active_quiz: Quiz) -> QuizResult:
    return await create_quiz_result(db, new_normal_user.id, new_active_quiz.id)
