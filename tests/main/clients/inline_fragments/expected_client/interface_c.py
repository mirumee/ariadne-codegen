from pydantic import Field

from .base_model import BaseModel


class InterfaceC(BaseModel):
    query_i: "InterfaceCQueryI" = Field(alias="queryI")


class InterfaceCQueryI(BaseModel):
    id: str


InterfaceC.update_forward_refs()
InterfaceCQueryI.update_forward_refs()
