from schema import Or, Schema

from zephyr.app.core.config import settings


class TestUserAuthentication:
    user_data = {
        "username": "zephyr",
        "password": "zephyr",
    }

    url_prefix = settings.API_V1_PREFIX

    def test_sign_up(self, test_app):
        response = test_app.post(
            f"{self.url_prefix}/auth/sign-up",
            json=self.user_data,
        )
        schema = Schema(
            {
                "id": Or(int, None),
                "uuid": str,
                "username": self.user_data["username"],
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

    def test_login_access_token(self, test_app):
        response = test_app.post(
            f"{self.url_prefix}/auth/login/access-token",
            data=self.user_data,
        )
        schema = Schema(
            {
                "access_token": str,
                "token_type": "bearer",
            }
        )

        assert response.status_code == 200
        assert schema.is_valid(response.json())
