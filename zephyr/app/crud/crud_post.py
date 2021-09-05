from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from zephyr.app.core.spotify import search_track_by_uri
from zephyr.app.crud.base import CRUDBase
from zephyr.app.models import Post, Track
from zephyr.app.schemas.post import PostCreate, TrackCreate


class CRUDPost(CRUDBase[Post, PostCreate, None]):
    pass


class CRUDTrack(CRUDBase[Track, TrackCreate, None]):
    def get_by_track_uri(self, db: Session, track_uri: str) -> Optional[Track]:
        return db.query(self.model).filter(self.model.uri == track_uri).first()

    def create_with_track_uri(self, db: Session, *, obj_in: TrackCreate) -> Track:
        track_uri = jsonable_encoder(obj_in)

        track_data = search_track_by_uri(track_uri)
        db_obj = self.model(**track_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


post = CRUDPost(Post)
track = CRUDTrack(Track)
