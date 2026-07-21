from typing import Optional

from .base_model import BaseModel


class GetUser(BaseModel):
    user: Optional["GetUserUser"]


class GetUserUser(BaseModel):
    id: str
    name: str
    friends: list["GetUserUserFriends"]


class GetUserUserFriends(BaseModel):
    id: str
    name: str
