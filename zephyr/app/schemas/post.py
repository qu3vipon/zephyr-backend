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

    class Config:
        orm_mode = True

    @validator("emoji")
    def check_emoji(cls, emoji):
        if len(emoji) > 1:
            raise ValueError("One emoji is allowed")

        if emoji not in EMOJI_UNICODE_ENGLISH.values():
            raise ValueError("Invalid emoji")
        return emoji


class TrackCreate(BaseModel):
    track_uri: str
