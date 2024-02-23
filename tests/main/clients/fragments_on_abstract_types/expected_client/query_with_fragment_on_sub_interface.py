from typing import Literal, Union

from pydantic import Field

from .base_model import BaseModel
from .fragments import FragmentA


class QueryWithFragmentOnSubInterface(BaseModel):
    query_interface: Union[
        "QueryWithFragmentOnSubInterfaceQueryInterfaceBaseInterface",
        "QueryWithFragmentOnSubInterfaceQueryInterfaceInterfaceA",
    ] = Field(alias="queryInterface", discriminator="typename__")


class QueryWithFragmentOnSubInterfaceQueryInterfaceBaseInterface(BaseModel):
    typename__: Literal["BaseInterface", "TypeA"] = Field(alias="__typename")


class QueryWithFragmentOnSubInterfaceQueryInterfaceInterfaceA(FragmentA):
    typename__: Literal["InterfaceA"] = Field(alias="__typename")


QueryWithFragmentOnSubInterface.model_rebuild()
QueryWithFragmentOnSubInterfaceQueryInterfaceBaseInterface.model_rebuild()
QueryWithFragmentOnSubInterfaceQueryInterfaceInterfaceA.model_rebuild()
