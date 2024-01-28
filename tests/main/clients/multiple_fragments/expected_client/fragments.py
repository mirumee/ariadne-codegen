from pydantic import Field

from .base_model import BaseModel


class CompleteA(BaseModel):
    id: str
    value: str
    field_b: "CompleteAFieldB" = Field(alias="fieldB")


class CompleteAFieldB(BaseModel):
    id: str
    value: float


class FullB(BaseModel):
    id: str
    value: float


class FullA(BaseModel):
    id: str
    value: str
    field_b: "FullAFieldB" = Field(alias="fieldB")


class FullAFieldB(FullB):
    pass


class MinimalB(BaseModel):
    id: str


class MinimalA(BaseModel):
    id: str
    field_b: "MinimalAFieldB" = Field(alias="fieldB")


class MinimalAFieldB(MinimalB):
    pass


CompleteA.model_rebuild()
FullB.model_rebuild()
FullA.model_rebuild()
MinimalB.model_rebuild()
MinimalA.model_rebuild()
