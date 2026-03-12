from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class ListStrings2(BaseModel):
    optional_list_string: Optional[list[str]] = Field(alias="optionalListString")
