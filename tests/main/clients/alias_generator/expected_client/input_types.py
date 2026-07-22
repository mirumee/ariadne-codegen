from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class UserFilter(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    some_field: Optional[str] = Field(alias="some_field", default=None)
    product_id: Optional[str] = Field(alias="productID", default=None)
    url: Optional[str] = Field(alias="URL", default=None)
    list_: Optional[list[str]] = Field(alias="list", default=None)
