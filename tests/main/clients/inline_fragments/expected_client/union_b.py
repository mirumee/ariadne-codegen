from typing import Union

from pydantic import Field

from .base_model import BaseModel


class UnionB(BaseModel):
    query_u: Union["UnionBQueryUTypeA", "UnionBQueryUTypeB"] = Field(alias="queryU")


class UnionBQueryUTypeA(BaseModel):
    typename__: str = Field(alias="__typename")
    id: str
    field_a: str = Field(alias="fieldA")


class UnionBQueryUTypeB(BaseModel):
    typename__: str = Field(alias="__typename")
    id: str


UnionB.update_forward_refs()
UnionBQueryUTypeA.update_forward_refs()
UnionBQueryUTypeB.update_forward_refs()
