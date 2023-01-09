from pydantic import Field

from .base_model import BaseModel


class TypeA(BaseModel):
    field_a: int = Field(alias="fieldA")


class TypeB(BaseModel):
    field_b: str = Field(alias="fieldB")


TypeA.update_forward_refs()
TypeB.update_forward_refs()
