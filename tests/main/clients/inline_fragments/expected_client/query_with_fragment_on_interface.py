from typing import Union

from pydantic import Field

from .base_model import BaseModel


class QueryWithFragmentOnInterface(BaseModel):
    query_i: Union[
        "QueryWithFragmentOnInterfaceQueryIInterface",
        "QueryWithFragmentOnInterfaceQueryITypeA",
        "QueryWithFragmentOnInterfaceQueryITypeB",
    ] = Field(alias="queryI")


class QueryWithFragmentOnInterfaceQueryIInterface(BaseModel):
    typename__: str = Field(alias="__typename")
    id: str


class QueryWithFragmentOnInterfaceQueryITypeA(BaseModel):
    typename__: str = Field(alias="__typename")
    id: str
    field_a: str = Field(alias="fieldA")


class QueryWithFragmentOnInterfaceQueryITypeB(BaseModel):
    typename__: str = Field(alias="__typename")
    id: str
    field_b: str = Field(alias="fieldB")


QueryWithFragmentOnInterface.update_forward_refs()
QueryWithFragmentOnInterfaceQueryIInterface.update_forward_refs()
QueryWithFragmentOnInterfaceQueryITypeA.update_forward_refs()
QueryWithFragmentOnInterfaceQueryITypeB.update_forward_refs()
