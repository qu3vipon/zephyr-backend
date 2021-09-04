from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from zephyr.app import crud, models, schemas
from zephyr.app.api import deps

router = APIRouter()


@router.post("/me/posts", status_code=201, response_model=schemas.Post)
def create_post(
    db: Session = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_user),
    track_uri: str = Body(...),
    emoji: str = Body(...),
):
    """
    Create new post
    """
    track = crud.track.get_by_track_uri(db, track_uri)
    if not track:
        track = crud.track.create_with_track_uri(db, obj_in=track_uri)

    # TODO: date validation -> 1 post a day
    post_data = schemas.PostCreate(user_id=user.id, emoji=emoji, track_id=track.id)
    post = crud.post.create(db, obj_in=post_data)
    return post
