from typing import Union

from pydantic import Field

from .base_model import BaseModel


class UnionA(BaseModel):
    query_u: Union["UnionAQueryUTypeA", "UnionAQueryUTypeB"] = Field(alias="queryU")


class UnionAQueryUTypeA(BaseModel):
    __typename__: str = Field(alias="__typename")
    id: str
    field_a: str = Field(alias="fieldA")


class UnionAQueryUTypeB(BaseModel):
    __typename__: str = Field(alias="__typename")
    id: str
    field_b: str = Field(alias="fieldB")


UnionA.update_forward_refs()
UnionAQueryUTypeA.update_forward_refs()
UnionAQueryUTypeB.update_forward_refs()
