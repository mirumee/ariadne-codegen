from typing import Literal

from pydantic import Field

from .base_model import BaseModel


class InterfaceC(BaseModel):
    query_i: "InterfaceCQueryI" = Field(alias="queryI")


class InterfaceCQueryI(BaseModel):
    typename__: Literal["Interface", "TypeA", "TypeB", "TypeC"] = Field(
        alias="__typename"
    )
    id: str
