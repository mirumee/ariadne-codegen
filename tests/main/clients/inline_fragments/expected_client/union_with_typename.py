from typing import Literal, Union

from pydantic import Field

from .base_model import BaseModel


class UnionWithTypename(BaseModel):
    query_u: Union[
        "UnionWithTypenameQueryUTypeA",
        "UnionWithTypenameQueryUTypeB",
        "UnionWithTypenameQueryUTypeC",
    ] = Field(alias="queryU", discriminator="typename__")


class UnionWithTypenameQueryUTypeA(BaseModel):
    typename__: Literal["TypeA"] = Field(alias="__typename")
    id: str


class UnionWithTypenameQueryUTypeB(BaseModel):
    typename__: Literal["TypeB"] = Field(alias="__typename")
    id: str


class UnionWithTypenameQueryUTypeC(BaseModel):
    typename__: Literal["TypeC"] = Field(alias="__typename")
    id: str


UnionWithTypename.update_forward_refs()
UnionWithTypenameQueryUTypeA.update_forward_refs()
UnionWithTypenameQueryUTypeB.update_forward_refs()
UnionWithTypenameQueryUTypeC.update_forward_refs()
