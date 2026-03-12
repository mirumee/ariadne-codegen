from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class ListStrings1(BaseModel):
    optional_list_optional_string: Optional[list[Optional[str]]] = Field(
        alias="optionalListOptionalString"
    )
