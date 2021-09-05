from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from zephyr.app.db.base import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    emoji = Column(String(4), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    track_id = Column(Integer, ForeignKey("tracks.id"))
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="posts")
    track = relationship("Track", back_populates="posts")


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    uri = Column(String(64), unique=True, index=True)
    name = Column(String)
    artists = Column(String)
    album_image = Column(String)
    preview_url = Column(String)

    posts = relationship("Post", back_populates="track")
