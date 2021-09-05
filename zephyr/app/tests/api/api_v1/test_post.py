from typing import Callable

import pytest
from schema import Or, Schema
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from zephyr.app import crud, models
from zephyr.app.core.config import settings

URL_PREFIX = settings.API_V1_PREFIX


class TestUserPosts:
    track_uri = "spotify:track:1fCeXjoRExPP2qwSBh2aST"

    def test_search_tracks(
        self,
        test_user: models.User,
        auth_token_headers: Callable,
        test_app: TestClient,
    ):
        query = "black"

        headers = auth_token_headers(test_user)
        response = test_app.post(
            f"{URL_PREFIX}/search/tracks?q={query}",
            headers=headers,
        )

        schema = Schema(
            [
                {
                    "uri": str,
                    "name": str,
                    "album_image": str,
                    "artists": str,
                    "preview_url": Or(str, None),
                }
            ]
        )

        assert response.status_code == 200
        assert schema.is_valid(response.json())

    def test_create_post(
        self,
        test_user: models.User,
        auth_token_headers: Callable,
        test_app: TestClient,
        db: Session,
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
                "created_at": str,
            }
        )

        assert response.status_code == 201
        assert schema.is_valid(response.json())

    @pytest.mark.parametrize(
        "emoji, error_message",
        [
            ("😀😀", "Multiple emojis are not allowed."),
            ("W", "Invalid emoji."),
        ],
    )
    def test_create_post_invalid_input(
        self,
        test_user: models.User,
        auth_token_headers: Callable,
        test_app: TestClient,
        emoji: str,
        error_message: str,
    ):
        with pytest.raises(ValueError) as excinfo:
            headers = auth_token_headers(test_user)
            test_app.post(
                f"{URL_PREFIX}/users/me/posts",
                headers=headers,
                json={"track_uri": self.track_uri, "emoji": emoji},
            )

        assert error_message in str(excinfo.value)
