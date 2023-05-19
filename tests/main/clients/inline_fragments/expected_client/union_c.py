from typing import Union

from pydantic import Field

from .base_model import BaseModel


class UnionC(BaseModel):
    query_u: Union["UnionCQueryUTypeA", "UnionCQueryUTypeB"] = Field(alias="queryU")


class UnionCQueryUTypeA(BaseModel):
    typename__: str = Field(alias="__typename")
    id: str


class UnionCQueryUTypeB(BaseModel):
    typename__: str = Field(alias="__typename")
    id: str


UnionC.update_forward_refs()
UnionCQueryUTypeA.update_forward_refs()
UnionCQueryUTypeB.update_forward_refs()
