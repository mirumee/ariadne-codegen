from typing import Literal, Union

from pydantic import Field

from .base_model import BaseModel


class FragmentOnQueryWithInterface(BaseModel):
    query_i: Union[
        "FragmentOnQueryWithInterfaceQueryIInterface",
        "FragmentOnQueryWithInterfaceQueryITypeA",
        "FragmentOnQueryWithInterfaceQueryITypeB",
    ] = Field(alias="queryI", discriminator="typename__")


class FragmentOnQueryWithInterfaceQueryIInterface(BaseModel):
    typename__: Literal["Interface", "TypeC"] = Field(alias="__typename")
    id: str


class FragmentOnQueryWithInterfaceQueryITypeA(BaseModel):
    typename__: Literal["TypeA"] = Field(alias="__typename")
    id: str
    field_a: str = Field(alias="fieldA")


class FragmentOnQueryWithInterfaceQueryITypeB(BaseModel):
    typename__: Literal["TypeB"] = Field(alias="__typename")
    id: str
    field_b: str = Field(alias="fieldB")


class FragmentOnQueryWithUnion(BaseModel):
    query_u: Union[
        "FragmentOnQueryWithUnionQueryUTypeA",
        "FragmentOnQueryWithUnionQueryUTypeB",
        "FragmentOnQueryWithUnionQueryUTypeC",
    ] = Field(alias="queryU", discriminator="typename__")


class FragmentOnQueryWithUnionQueryUTypeA(BaseModel):
    typename__: Literal["TypeA"] = Field(alias="__typename")
    id: str
    field_a: str = Field(alias="fieldA")


class FragmentOnQueryWithUnionQueryUTypeB(BaseModel):
    typename__: Literal["TypeB"] = Field(alias="__typename")
    id: str
    field_b: str = Field(alias="fieldB")


class FragmentOnQueryWithUnionQueryUTypeC(BaseModel):
    typename__: Literal["TypeC"] = Field(alias="__typename")


class UnusedFragmentOnTypeA(BaseModel):
    id: str
    field_a: str = Field(alias="fieldA")


FragmentOnQueryWithInterface.update_forward_refs()
FragmentOnQueryWithInterfaceQueryIInterface.update_forward_refs()
FragmentOnQueryWithInterfaceQueryITypeA.update_forward_refs()
FragmentOnQueryWithInterfaceQueryITypeB.update_forward_refs()
FragmentOnQueryWithUnion.update_forward_refs()
FragmentOnQueryWithUnionQueryUTypeA.update_forward_refs()
FragmentOnQueryWithUnionQueryUTypeB.update_forward_refs()
FragmentOnQueryWithUnionQueryUTypeC.update_forward_refs()
UnusedFragmentOnTypeA.update_forward_refs()
