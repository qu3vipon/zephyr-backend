from datetime import datetime

import pytz
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from zephyr.app import crud, models, schemas
from zephyr.app.api import deps

router = APIRouter()


@router.post("/me/posts", status_code=201, response_model=schemas.Post)
def create_post(
    db: Session = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
    timezone: pytz.timezone = Depends(deps.get_timezone),
    track_uri: str = Body(...),
    emoji: str = Body(...),
):
    """
    Create new post
    """

    last_post = crud.post.get_last(db, user)
    if last_post:
        last_upload = last_post.created_at
        last_upload_local: datetime = pytz.utc.localize(last_upload).astimezone(
            timezone
        )
        last_upload_date = last_upload_local.date()

        local_now: datetime = pytz.utc.localize(datetime.utcnow()).astimezone(timezone)
        local_today = local_now.date()

        if last_upload_date >= local_today:
            raise HTTPException(
                status_code=400, detail="You can upload one post a day."
            )

    track = crud.track.get_by_track_uri(db, track_uri)
    if not track:
        track = crud.track.create_with_track_uri(db, obj_in=track_uri)

    post_data = schemas.PostCreate(user_id=user.id, emoji=emoji, track_id=track.id)
    post = crud.post.create(db, obj_in=post_data)
    return post
