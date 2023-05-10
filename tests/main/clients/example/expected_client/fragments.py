from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class BasicUser(BaseModel):
    id: str
    email: str


class UserPersonalData(BaseModel):
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")


BasicUser.update_forward_refs()
UserPersonalData.update_forward_refs()
