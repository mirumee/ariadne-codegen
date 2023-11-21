from typing import Literal, Union

from pydantic import Field

from .base_model import BaseModel


class QueryWithFragmentOnSubInterfaceWithInlineFragment(BaseModel):
    query_interface: Union[
        "QueryWithFragmentOnSubInterfaceWithInlineFragmentQueryInterfaceBaseInterface",
        "QueryWithFragmentOnSubInterfaceWithInlineFragmentQueryInterfaceInterfaceA",
        "QueryWithFragmentOnSubInterfaceWithInlineFragmentQueryInterfaceTypeA",
    ] = Field(alias="queryInterface", discriminator="typename__")


class QueryWithFragmentOnSubInterfaceWithInlineFragmentQueryInterfaceBaseInterface(
    BaseModel
):
    typename__: Literal["BaseInterface"] = Field(alias="__typename")


class QueryWithFragmentOnSubInterfaceWithInlineFragmentQueryInterfaceInterfaceA(
    BaseModel
):
    typename__: Literal["InterfaceA"] = Field(alias="__typename")
    id: str
    value_a: str = Field(alias="valueA")


class QueryWithFragmentOnSubInterfaceWithInlineFragmentQueryInterfaceTypeA(BaseModel):
    typename__: Literal["TypeA"] = Field(alias="__typename")
    id: str
    value_a: str = Field(alias="valueA")
    another: str
