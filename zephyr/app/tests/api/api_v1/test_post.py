from typing import Callable

from schema import Schema
from starlette.testclient import TestClient

from zephyr.app import crud
from zephyr.app.core.config import settings

URL_PREFIX = settings.API_V1_PREFIX


class TestUserPosts:
    track_uri = "spotify:track:1fCeXjoRExPP2qwSBh2aST"

    def test_create_post(
        self,
        db,
        test_app: TestClient,
        auth_token_headers: Callable,
        test_user,
    ):
        headers = auth_token_headers(test_user)
        response = test_app.post(
            f"{URL_PREFIX}/users/me/posts",
            headers=headers,
            json={"track_uri": self.track_uri, "emoji": "😀"},
        )

        track = crud.track.get_by_track_uri(db, track_uri=self.track_uri)
        assert track

        schema = Schema(
            {
                "id": int,
                "emoji": "😀",
                "user_id": test_user.id,
                "track_id": track.id,
            }
        )

        assert response.status_code == 201
        assert schema.is_valid(response.json())
