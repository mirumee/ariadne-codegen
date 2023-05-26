from typing import Literal, Union

from pydantic import Field

from .base_model import BaseModel


class UnionC(BaseModel):
    query_u: Union[
        "UnionCQueryUTypeA", "UnionCQueryUTypeB", "UnionCQueryUTypeC"
    ] = Field(alias="queryU", discriminator="typename__")


class UnionCQueryUTypeA(BaseModel):
    typename__: Literal["TypeA"] = Field(alias="__typename")
    id: str


class UnionCQueryUTypeB(BaseModel):
    typename__: Literal["TypeB"] = Field(alias="__typename")
    id: str


class UnionCQueryUTypeC(BaseModel):
    typename__: Literal["TypeC"] = Field(alias="__typename")
    id: str


UnionC.update_forward_refs()
UnionCQueryUTypeA.update_forward_refs()
UnionCQueryUTypeB.update_forward_refs()
UnionCQueryUTypeC.update_forward_refs()
