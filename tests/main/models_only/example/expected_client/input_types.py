from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import Color


class UserCreateInput(BaseModel):
    first_name: Optional[str] = Field(alias="firstName", default=None)
    last_name: Optional[str] = Field(alias="lastName", default=None)
    email: str
    favourite_color: Optional[Color] = Field(alias="favouriteColor", default=None)
