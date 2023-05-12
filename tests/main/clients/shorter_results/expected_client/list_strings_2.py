from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class ListStrings2(BaseModel):
    optional_list_string: Optional[List[str]] = Field(alias="optionalListString")


ListStrings2.update_forward_refs()
