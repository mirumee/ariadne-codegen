from typing import Literal, Union

from pydantic import Field

from .base_model import BaseModel


class QueryWithFragmentOnUnion(BaseModel):
    query_u: Union[
        "QueryWithFragmentOnUnionQueryUTypeA",
        "QueryWithFragmentOnUnionQueryUTypeB",
        "QueryWithFragmentOnUnionQueryUTypeC",
    ] = Field(alias="queryU", discriminator="typename__")


class QueryWithFragmentOnUnionQueryUTypeA(BaseModel):
    typename__: Literal["TypeA"] = Field(alias="__typename")
    id: str
    field_a: str = Field(alias="fieldA")


class QueryWithFragmentOnUnionQueryUTypeB(BaseModel):
    typename__: Literal["TypeB"] = Field(alias="__typename")
    id: str
    field_b: str = Field(alias="fieldB")


class QueryWithFragmentOnUnionQueryUTypeC(BaseModel):
    typename__: Literal["TypeC"] = Field(alias="__typename")


QueryWithFragmentOnUnion.model_rebuild()
