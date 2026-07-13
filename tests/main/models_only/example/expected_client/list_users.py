from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import Color


class ListUsers(BaseModel):
    users: list["ListUsersUsers"]


class ListUsersUsers(BaseModel):
    id: str
    first_name: Optional[str] = Field(alias="firstName")
    email: str
    favourite_color: Optional[Color] = Field(alias="favouriteColor")


ListUsers.model_rebuild()
