from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class Item(BaseModel):
    id: Optional[str]


class ItemError(BaseModel):
    typename__: str = Field(alias="__typename")
    message: str


Item.model_rebuild()
ItemError.model_rebuild()
