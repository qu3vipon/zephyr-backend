from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    is_active: Optional[bool] = True


# Properties to receive via API on creation
class UserCreate(BaseModel):
    username: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(BaseModel):
    id: Optional[int] = None
    uuid: UUID
    username: str
    password_hash: str
    is_active: bool
    is_superuser: bool
    registered_at: datetime
    unregistered_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class UserOut(UserInDBBase):
    access_token: str
