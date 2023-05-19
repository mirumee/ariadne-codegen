from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class ListStrings3(BaseModel):
    list_optional_string: List[Optional[str]] = Field(alias="listOptionalString")


ListStrings3.update_forward_refs()
