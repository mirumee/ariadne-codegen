from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class ListTypeA(BaseModel):
    list_optional_type_a: List[Optional["ListTypeAListOptionalTypeA"]] = Field(
        alias="listOptionalTypeA"
    )


class ListTypeAListOptionalTypeA(BaseModel):
    id: int


ListTypeA.update_forward_refs()
ListTypeAListOptionalTypeA.update_forward_refs()
