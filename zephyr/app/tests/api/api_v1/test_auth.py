from schema import Or, Schema

from zephyr.app.core import security
from zephyr.app.core.config import settings


class TestUserAuthentication:
    new_user_body = {
        "username": "zephyr2",
        "password": "zephyr2",
    }

    url_prefix: str = settings.API_V1_PREFIX

    def test_sign_up(self, test_app):
        response = test_app.post(
            f"{self.url_prefix}/auth/sign-up",
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

    def test_login_access_token(self, test_app, test_user):
        response = test_app.post(
            f"{self.url_prefix}/auth/login/access-token",
            data=self.new_user_body,
        )
        schema = Schema(
            {
                "access_token": str,
                "token_type": "bearer",
            }
        )

        assert response.status_code == 200
        schema.validate(response.json())
        assert schema.is_valid(response.json())

    def test_reset_password(self, test_app, test_user):
        access_token = security.create_access_token(test_user.uuid)
        reset_body = {
            "access_token": access_token,
            "new_password": "new_password",
        }
        response = test_app.post(
            f"{self.url_prefix}/auth/reset-password", json=reset_body
        )

        assert response.status_code == 200
        assert response.json()["msg"] == "Password updated successfully."

        login_body = {
            "username": test_user.username,
            "password": reset_body["new_password"],
        }
        response = test_app.post(
            f"{self.url_prefix}/auth/login/access-token",
            data=login_body,
        )

        assert response.status_code == 200
