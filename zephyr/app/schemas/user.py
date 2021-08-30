from typing import Optional

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
