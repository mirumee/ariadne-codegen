from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import Color
from .fragments import BasicUser, UserPersonalData


class ListUsersByCountry(BaseModel):
    users: List["ListUsersByCountryUsers"]


class ListUsersByCountryUsers(BasicUser, UserPersonalData):
    favourite_color: Optional[Color] = Field(alias="favouriteColor")


ListUsersByCountry.model_rebuild()
