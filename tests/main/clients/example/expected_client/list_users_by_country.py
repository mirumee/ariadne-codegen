from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import Color


class ListUsersByCountry(BaseModel):
    users: List["ListUsersByCountryUsers"]


class ListUsersByCountryUsers(BaseModel):
    id: str
    email: str
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
    favourite_color: Optional[Color] = Field(alias="favouriteColor")


ListUsersByCountry.update_forward_refs()
ListUsersByCountryUsers.update_forward_refs()
