from typing import Literal

from pydantic import Field

from .base_model import BaseModel


class InterfaceWithTypename(BaseModel):
    query_i: "InterfaceWithTypenameQueryI" = Field(alias="queryI")


class InterfaceWithTypenameQueryI(BaseModel):
    typename__: Literal["Interface", "TypeA", "TypeB", "TypeC"] = Field(
        alias="__typename"
    )
    id: str


InterfaceWithTypename.update_forward_refs()
InterfaceWithTypenameQueryI.update_forward_refs()
