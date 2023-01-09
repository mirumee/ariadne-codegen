from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import Color


class User(BaseModel):
    id: str
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
    email: str
    favourite_color: Optional["Color"] = Field(alias="favouriteColor")
    location: Optional["Location"]


class Location(BaseModel):
    city: Optional[str]
    country: Optional[str]


User.update_forward_refs()
Location.update_forward_refs()
