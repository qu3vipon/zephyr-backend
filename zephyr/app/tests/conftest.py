from typing import Generator

import pytest
from starlette.testclient import TestClient

from zephyr.app import crud
from zephyr.app.core.config import Settings, get_settings
from zephyr.app.db.session import SessionLocal
from zephyr.app.main import app
from zephyr.app.schemas import UserCreate


def get_settings_override():
    return Settings(ENVIRONMENT="test", TESTING=1)


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def test_app():
    # set up
    app.dependency_overrides[get_settings] = get_settings_override()
    with TestClient(app) as test_client:
        # testing
        yield test_client

    # tear down


@pytest.fixture(scope="class")
def test_user(db):
    user_in = UserCreate(username="zephyr", password="zephyr")
    user = crud.user.create(db=db, obj_in=user_in)
    return user
