from typing import Generator

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core import config
from app.database.base_class import Base
from app.main import get_application


@pytest.fixture(scope="session")
def db() -> Generator:
    engine = create_engine(config.TEST_DB_DEFAULT)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        engine.dispose()


@pytest.fixture(scope="module")
def client() -> Generator:
    app = get_application()
    with TestClient(app) as c:
        yield c
