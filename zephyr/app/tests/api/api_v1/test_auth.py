from schema import Or, Schema
from starlette.testclient import TestClient

from zephyr.app import models
from zephyr.app.core import security
from zephyr.app.core.config import settings

URL_PREFIX = settings.API_V1_PREFIX


class TestUserAuthentication:
    new_user_body = {
        "username": "zephyr2",
        "password": "zephyr2",
    }

    def test_sign_up(self, test_app: TestClient):
        response = test_app.post(
            f"{URL_PREFIX}/auth/sign-up",
            json=self.new_user_body,
        )
        schema = Schema(
            {
                "id": Or(int, None),
                "uuid": str,
                "username": self.new_user_body["username"],
                "password_hash": str,
                "is_active": True,
                "is_superuser": False,
                "registered_at": str,
                "unregistered_at": Or(str, None),
                "access_token": str,
            }
        )

        assert response.status_code == 201
        assert schema.is_valid(response.json())

    def test_login_access_token(self, test_app: TestClient):
        response = test_app.post(
            f"{URL_PREFIX}/auth/login/access-token",
            data=self.new_user_body,
        )
        schema = Schema(
            {
                "access_token": str,
                "token_type": "bearer",
            }
        )

        assert response.status_code == 200
        assert schema.is_valid(response.json())

    def test_reset_password(self, test_app: TestClient, test_user: models.User):
        access_token = security.create_access_token(test_user.id)
        new_password = "new_password"

        reset_body = {
            "access_token": access_token,
            "new_password": new_password,
        }
        response = test_app.post(f"{URL_PREFIX}/auth/reset-password", json=reset_body)

        assert response.status_code == 200
        assert response.json()["msg"] == "Password updated successfully."

        login_request_body = {
            "username": test_user.username,
            "password": new_password,
        }
        response = test_app.post(
            f"{URL_PREFIX}/auth/login/access-token",
            data=login_request_body,
        )

        assert response.status_code == 200
