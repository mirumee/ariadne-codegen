from typing import Literal, Union

from pydantic import Field

from .base_model import BaseModel


class UnionB(BaseModel):
    query_u: Union[
        "UnionBQueryUTypeA", "UnionBQueryUTypeB", "UnionBQueryUTypeC"
    ] = Field(alias="queryU", discriminator="typename__")


class UnionBQueryUTypeA(BaseModel):
    typename__: Literal["TypeA"] = Field(alias="__typename")
    id: str
    field_a: str = Field(alias="fieldA")


class UnionBQueryUTypeB(BaseModel):
    typename__: Literal["TypeB"] = Field(alias="__typename")


class UnionBQueryUTypeC(BaseModel):
    typename__: Literal["TypeC"] = Field(alias="__typename")


UnionB.update_forward_refs()
UnionBQueryUTypeA.update_forward_refs()
UnionBQueryUTypeB.update_forward_refs()
UnionBQueryUTypeC.update_forward_refs()
