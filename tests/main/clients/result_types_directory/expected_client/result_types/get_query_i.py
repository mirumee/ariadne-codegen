from typing import Any

from pydantic import Field

from ..base_model import BaseModel


class GetQueryI(BaseModel):
    query_i: "GetQueryIQueryI" = Field(alias="queryI")


class GetQueryIQueryI(BaseModel):
    field_i: int = Field(alias="fieldI")
    date: Any
