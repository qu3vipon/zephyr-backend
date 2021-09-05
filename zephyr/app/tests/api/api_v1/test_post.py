from typing import Callable, Optional

import pytest
from schema import Or, Schema
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from zephyr.app import crud, models
from zephyr.app.core.config import settings

URL_PREFIX = settings.API_V1_PREFIX


class TestUserPosts:
    track_uri = "spotify:track:1fCeXjoRExPP2qwSBh2aST"
    created_post_id: Optional[int] = None

    def test_search_tracks(
        self,
        test_user: models.User,
        auth_token_header: Callable,
        timezone_header: dict,
        test_app: TestClient,
    ):
        query = "black"

        headers = auth_token_header(test_user)
        headers.update(timezone_header)
        response = test_app.get(
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
        auth_token_header: Callable,
        timezone_header: dict,
        test_app: TestClient,
        emoji: str,
        error_message: str,
        db: Session,
    ):
        last_post = crud.post.get_last(db, user=test_user)
        if last_post:
            crud.post.remove(db, id=last_post.id)

        with pytest.raises(ValueError) as excinfo:
            headers = auth_token_header(test_user)
            headers.update(timezone_header)
            test_app.post(
                f"{URL_PREFIX}/users/me/posts",
                headers=headers,
                json={"track_uri": self.track_uri, "emoji": emoji},
            )

        assert error_message in str(excinfo.value)

    def test_create_post(
        self,
        test_user: models.User,
        auth_token_header: Callable,
        timezone_header: dict,
        test_app: TestClient,
        db: Session,
    ):
        last_post = crud.post.get_last(db, user=test_user)
        if last_post:
            crud.post.remove(db, id=last_post.id)

        headers = auth_token_header(test_user)
        headers.update(timezone_header)
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

        schema.validate(response.json())

        assert response.status_code == 201
        assert schema.is_valid(response.json())

    def test_create_post_fail(
        self,
        test_user: models.User,
        auth_token_header: Callable,
        timezone_header: dict,
        test_app: TestClient,
    ):
        headers = auth_token_header(test_user)
        headers.update(timezone_header)
        response = test_app.post(
            f"{URL_PREFIX}/users/me/posts",
            headers=headers,
            json={"track_uri": self.track_uri, "emoji": "😀"},
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "You can upload one post a day."
