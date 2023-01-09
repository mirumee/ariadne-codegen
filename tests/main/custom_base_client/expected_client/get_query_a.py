from pydantic import Field

from .base_model import BaseModel


class GetQueryA(BaseModel):
    query_a: "GetQueryAQueryA" = Field(alias="queryA")


class GetQueryAQueryA(BaseModel):
    field_a: int = Field(alias="fieldA")


GetQueryA.update_forward_refs()
GetQueryAQueryA.update_forward_refs()
