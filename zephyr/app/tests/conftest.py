import os

import pytest
from starlette.testclient import TestClient

from zephyr.app.main import app
from zephyr.app.core.config import Settings, get_settings


def get_settings_override():
    return Settings(ENVIRONMENT="test", TESTING=1)


@pytest.fixture(scope="module")
def test_app():
    # set up
    app.dependency_overrides[get_settings] = get_settings_override()
    with TestClient(app) as test_client:
        # testing
        yield test_client

    # tear down
