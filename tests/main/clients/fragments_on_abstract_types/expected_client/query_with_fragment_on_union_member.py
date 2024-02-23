from typing import Literal, Union

from pydantic import Field

from .base_model import BaseModel
from .fragments import FragmentB


class QueryWithFragmentOnUnionMember(BaseModel):
    query_union: Union[
        "QueryWithFragmentOnUnionMemberQueryUnionTypeA",
        "QueryWithFragmentOnUnionMemberQueryUnionTypeB",
    ] = Field(alias="queryUnion", discriminator="typename__")


class QueryWithFragmentOnUnionMemberQueryUnionTypeA(BaseModel):
    typename__: Literal["TypeA"] = Field(alias="__typename")


class QueryWithFragmentOnUnionMemberQueryUnionTypeB(FragmentB):
    typename__: Literal["TypeB"] = Field(alias="__typename")


QueryWithFragmentOnUnionMember.model_rebuild()
QueryWithFragmentOnUnionMemberQueryUnionTypeA.model_rebuild()
QueryWithFragmentOnUnionMemberQueryUnionTypeB.model_rebuild()
