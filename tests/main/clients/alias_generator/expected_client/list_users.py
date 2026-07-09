from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class ListUsers(BaseModel):
    users: list["ListUsersUsers"]


class ListUsersUsers(BaseModel):
    id: str
    first_name: Optional[str]
    last_name: Optional[str]
    some_field: Optional[str] = Field(alias="some_field")
    product_id: Optional[str] = Field(alias="productID")
    url: Optional[str] = Field(alias="URL")


ListUsers.model_rebuild()
