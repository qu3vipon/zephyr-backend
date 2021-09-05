from typing import Callable, Dict, Generator

import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from zephyr.app import crud, models
from zephyr.app.core.config import Settings, get_settings, settings
from zephyr.app.core.security import create_access_token
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
def test_user(db: Session) -> Generator:
    user_in = UserCreate(
        username=settings.TEST_USERNAME, password=settings.TEST_PASSWORD
    )
    user = crud.user.create(db, obj_in=user_in)
    yield user
    db.delete(user)


@pytest.fixture(scope="session")
def auth_token_header(test_app: TestClient, db: Session) -> Callable:
    def _auth_token_header(user: models.User) -> Dict[str, str]:
        token = create_access_token(user.id)
        headers = {"Authorization": f"Bearer {token}"}
        return headers

    return _auth_token_header


@pytest.fixture(scope="session")
def timezone_header() -> Dict[str, str]:
    return {"X-Timezone": "Asia/Seoul"}
