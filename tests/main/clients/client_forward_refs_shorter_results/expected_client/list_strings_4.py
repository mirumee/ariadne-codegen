from pydantic import Field

from .base_model import BaseModel


class ListStrings4(BaseModel):
    list_string: list[str] = Field(alias="listString")
