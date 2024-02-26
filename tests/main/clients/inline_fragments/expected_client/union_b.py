from typing import Literal, Union

from pydantic import Field

from .base_model import BaseModel


class UnionB(BaseModel):
    query_u: Union["UnionBQueryUTypeA", "UnionBQueryUTypeB", "UnionBQueryUTypeC"] = (
        Field(alias="queryU", discriminator="typename__")
    )


class UnionBQueryUTypeA(BaseModel):
    typename__: Literal["TypeA"] = Field(alias="__typename")
    id: str
    field_a: str = Field(alias="fieldA")


class UnionBQueryUTypeB(BaseModel):
    typename__: Literal["TypeB"] = Field(alias="__typename")


class UnionBQueryUTypeC(BaseModel):
    typename__: Literal["TypeC"] = Field(alias="__typename")


UnionB.model_rebuild()
UnionB.model_rebuild()
UnionB.model_rebuild()
UnionBQueryUTypeA.model_rebuild()
UnionBQueryUTypeB.model_rebuild()
UnionBQueryUTypeC.model_rebuild()
