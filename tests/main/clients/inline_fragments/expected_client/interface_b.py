from typing import Literal, Union

from pydantic import Field

from .base_model import BaseModel


class InterfaceB(BaseModel):
    query_i: Union["InterfaceBQueryIInterface", "InterfaceBQueryITypeA"] = Field(
        alias="queryI", discriminator="typename__"
    )


class InterfaceBQueryIInterface(BaseModel):
    typename__: Literal["Interface", "TypeB", "TypeC"] = Field(alias="__typename")
    id: str


class InterfaceBQueryITypeA(BaseModel):
    typename__: Literal["TypeA"] = Field(alias="__typename")
    id: str
    field_a: str = Field(alias="fieldA")


InterfaceB.update_forward_refs()
InterfaceBQueryIInterface.update_forward_refs()
InterfaceBQueryITypeA.update_forward_refs()
