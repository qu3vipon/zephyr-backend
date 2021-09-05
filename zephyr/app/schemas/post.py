from datetime import datetime

from emoji.unicode_codes.en import EMOJI_UNICODE_ENGLISH
from pydantic import BaseModel, validator


class PostCreate(BaseModel):
    user_id: int
    track_id: int
    emoji: str


class Post(BaseModel):
    id: int
    emoji: str
    user_id: int
    track_id: int
    created_at: datetime

    class Config:
        orm_mode = True

    @validator("emoji")
    def check_emoji(cls, emoji):
        if len(emoji) > 1:
            raise ValueError("Multiple emojis are not allowed.")

        if emoji not in EMOJI_UNICODE_ENGLISH.values():
            raise ValueError("Invalid emoji.")
        return emoji


class TrackCreate(BaseModel):
    track_uri: str
