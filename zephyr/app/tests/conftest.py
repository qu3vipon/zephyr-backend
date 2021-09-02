from typing import Generator

import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from zephyr.app import crud
from zephyr.app.core.config import Settings, get_settings
from zephyr.app.db.base import Base
from zephyr.app.db.session import SessionLocal, engine
from zephyr.app.main import app
from zephyr.app.schemas import UserCreate


def get_settings_override():
    return Settings(ENVIRONMENT="test", TESTING=1)


def pytest_sessionfinish():
    # revert all tables at the end of tests
    from zephyr.app.models import __all_models  # noqa

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def db() -> Generator:
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="session")
def test_app() -> Generator:
    app.dependency_overrides[get_settings] = get_settings_override()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def test_user_raw_password(db: Session) -> str:
    return "zephyr"


@pytest.fixture(scope="class")
def test_user(db: Session, test_user_raw_password: str) -> Generator:
    user_in = UserCreate(username="zephyr", password=test_user_raw_password)
    user = crud.user.create(db=db, obj_in=user_in)
    yield user
    db.delete(user)
