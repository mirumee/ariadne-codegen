from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class ListAllUsers(BaseModel):
    users: List["ListAllUsersUsers"]


class ListAllUsersUsers(BaseModel):
    id: str
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
    email: str
    location: Optional["ListAllUsersUsersLocation"]


class ListAllUsersUsersLocation(BaseModel):
    country: Optional[str]


ListAllUsers.model_rebuild()
ListAllUsersUsers.model_rebuild()
ListAllUsersUsersLocation.model_rebuild()
