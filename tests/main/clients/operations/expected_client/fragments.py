from pydantic import Field

from .base_model import BaseModel


class FragmentB(BaseModel):
    value: str


class FragmentY(BaseModel):
    value_y: int = Field(alias="valueY")
