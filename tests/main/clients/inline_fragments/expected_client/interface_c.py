from pydantic import Field

from .base_model import BaseModel


class InterfaceC(BaseModel):
    query_i: "InterfaceCQueryI" = Field(alias="queryI")


class InterfaceCQueryI(BaseModel):
    id: str


InterfaceC.model_rebuild()
InterfaceCQueryI.model_rebuild()
