from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class ListStrings3(BaseModel):
    list_optional_string: list[Optional[str]] = Field(alias="listOptionalString")
