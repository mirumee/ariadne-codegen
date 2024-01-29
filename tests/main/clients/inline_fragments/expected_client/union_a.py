from typing import Literal, Union

from pydantic import Field

from .base_model import BaseModel


class UnionA(BaseModel):
    query_u: Union["UnionAQueryUTypeA", "UnionAQueryUTypeB", "UnionAQueryUTypeC"] = (
        Field(alias="queryU", discriminator="typename__")
    )


class UnionAQueryUTypeA(BaseModel):
    typename__: Literal["TypeA"] = Field(alias="__typename")
    id: str
    field_a: str = Field(alias="fieldA")


class UnionAQueryUTypeB(BaseModel):
    typename__: Literal["TypeB"] = Field(alias="__typename")
    id: str
    field_b: str = Field(alias="fieldB")


class UnionAQueryUTypeC(BaseModel):
    typename__: Literal["TypeC"] = Field(alias="__typename")
