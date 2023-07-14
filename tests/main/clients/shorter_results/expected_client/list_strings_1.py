from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class ListStrings1(BaseModel):
    optional_list_optional_string: Optional[List[Optional[str]]] = Field(
        alias="optionalListOptionalString"
    )


ListStrings1.model_rebuild()
