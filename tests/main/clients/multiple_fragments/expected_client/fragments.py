from pydantic import Field

from .base_model import BaseModel


class MinimalB(BaseModel):
    id: str


class MinimalA(BaseModel):
    id: str
    field_b: "MinimalAFieldB" = Field(alias="fieldB")


class MinimalAFieldB(MinimalB):
    pass


class FullB(BaseModel):
    id: str
    value: float


class FullA(BaseModel):
    id: str
    value: str
    field_b: "FullAFieldB" = Field(alias="fieldB")


class FullAFieldB(FullB):
    pass


class CompleteA(BaseModel):
    id: str
    value: str
    field_b: "CompleteAFieldB" = Field(alias="fieldB")


class CompleteAFieldB(BaseModel):
    id: str
    value: float


MinimalB.update_forward_refs()
MinimalA.update_forward_refs()
MinimalAFieldB.update_forward_refs()
FullB.update_forward_refs()
FullA.update_forward_refs()
FullAFieldB.update_forward_refs()
CompleteA.update_forward_refs()
CompleteAFieldB.update_forward_refs()
