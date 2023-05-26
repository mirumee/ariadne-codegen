from typing import Literal, Union

from pydantic import Field

from .base_model import BaseModel


class InterfaceA(BaseModel):
    query_i: Union[
        "InterfaceAQueryIInterface", "InterfaceAQueryITypeA", "InterfaceAQueryITypeB"
    ] = Field(alias="queryI", discriminator="typename__")


class InterfaceAQueryIInterface(BaseModel):
    typename__: Literal["Interface", "TypeC"] = Field(alias="__typename")
    id: str


class InterfaceAQueryITypeA(BaseModel):
    typename__: Literal["TypeA"] = Field(alias="__typename")
    id: str
    field_a: str = Field(alias="fieldA")


class InterfaceAQueryITypeB(BaseModel):
    typename__: Literal["TypeB"] = Field(alias="__typename")
    id: str
    field_b: str = Field(alias="fieldB")


InterfaceA.update_forward_refs()
InterfaceAQueryIInterface.update_forward_refs()
InterfaceAQueryITypeA.update_forward_refs()
InterfaceAQueryITypeB.update_forward_refs()
