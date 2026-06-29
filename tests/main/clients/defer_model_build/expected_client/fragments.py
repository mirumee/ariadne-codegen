from .base_model import BaseModel


class UserFields(BaseModel):
    id: str
    name: str
    friends: list["UserFieldsFriends"]


class UserFieldsFriends(BaseModel):
    id: str
    name: str
