from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class SubscribeStrings(BaseModel):
    optional_list_string: Optional[List[str]] = Field(alias="optionalListString")


SubscribeStrings.model_rebuild()
