from pydantic import Field

from .base_model import BaseModel


class FragmentA(BaseModel):
    id: str
    value_a: str = Field(alias="valueA")


class FragmentB(BaseModel):
    id: str
    value_b: str = Field(alias="valueB")


FragmentA.model_rebuild()
FragmentB.model_rebuild()
