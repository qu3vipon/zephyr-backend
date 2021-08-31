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

        assert response.status_code == 200

    def test_login_access_token(self, test_app):
        response = test_app.post(
            f"{self.url_prefix}/auth/login/access-token",
            data=self.user_data,
        )

        assert response.status_code == 200
        assert "access_token" in response.json()
