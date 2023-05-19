from typing import Union

from pydantic import Field

from .base_model import BaseModel


class FragmentOnQueryWithInterface(BaseModel):
    query_i: Union[
        "FragmentOnQueryWithInterfaceQueryIInterface",
        "FragmentOnQueryWithInterfaceQueryITypeA",
        "FragmentOnQueryWithInterfaceQueryITypeB",
    ] = Field(alias="queryI")


class FragmentOnQueryWithInterfaceQueryIInterface(BaseModel):
    typename__: str = Field(alias="__typename")
    id: str


class FragmentOnQueryWithInterfaceQueryITypeA(BaseModel):
    typename__: str = Field(alias="__typename")
    id: str
    field_a: str = Field(alias="fieldA")


class FragmentOnQueryWithInterfaceQueryITypeB(BaseModel):
    typename__: str = Field(alias="__typename")
    id: str
    field_b: str = Field(alias="fieldB")


class FragmentOnQueryWithUnion(BaseModel):
    query_u: Union[
        "FragmentOnQueryWithUnionQueryUTypeA", "FragmentOnQueryWithUnionQueryUTypeB"
    ] = Field(alias="queryU")


class FragmentOnQueryWithUnionQueryUTypeA(BaseModel):
    typename__: str = Field(alias="__typename")
    id: str
    field_a: str = Field(alias="fieldA")


class FragmentOnQueryWithUnionQueryUTypeB(BaseModel):
    typename__: str = Field(alias="__typename")
    id: str
    field_b: str = Field(alias="fieldB")


FragmentOnQueryWithInterface.update_forward_refs()
FragmentOnQueryWithInterfaceQueryIInterface.update_forward_refs()
FragmentOnQueryWithInterfaceQueryITypeA.update_forward_refs()
FragmentOnQueryWithInterfaceQueryITypeB.update_forward_refs()
FragmentOnQueryWithUnion.update_forward_refs()
FragmentOnQueryWithUnionQueryUTypeA.update_forward_refs()
FragmentOnQueryWithUnionQueryUTypeB.update_forward_refs()
