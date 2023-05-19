from typing import List

from pydantic import Field

from .base_model import BaseModel


class ListStrings4(BaseModel):
    list_string: List[str] = Field(alias="listString")


ListStrings4.update_forward_refs()
