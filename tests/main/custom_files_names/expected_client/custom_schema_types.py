from pydantic import Field

from .base_model import BaseModel


class TypeA(BaseModel):
    field_a: int = Field(alias="fieldA")


TypeA.update_forward_refs()
