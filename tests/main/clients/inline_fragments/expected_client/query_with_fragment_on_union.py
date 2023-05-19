from typing import Union

from pydantic import Field

from .base_model import BaseModel


class QueryWithFragmentOnUnion(BaseModel):
    query_u: Union[
        "QueryWithFragmentOnUnionQueryUTypeA", "QueryWithFragmentOnUnionQueryUTypeB"
    ] = Field(alias="queryU")


class QueryWithFragmentOnUnionQueryUTypeA(BaseModel):
    typename__: str = Field(alias="__typename")
    id: str
    field_a: str = Field(alias="fieldA")


class QueryWithFragmentOnUnionQueryUTypeB(BaseModel):
    typename__: str = Field(alias="__typename")
    id: str
    field_b: str = Field(alias="fieldB")


QueryWithFragmentOnUnion.update_forward_refs()
QueryWithFragmentOnUnionQueryUTypeA.update_forward_refs()
QueryWithFragmentOnUnionQueryUTypeB.update_forward_refs()
