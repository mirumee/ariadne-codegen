from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import EnumE


class InputA(BaseModel):
    value_aa: "InputAA" = Field(alias="valueAA")
    value_ab: Optional["InputAB"] = Field(alias="valueAB", default=None)


class InputAA(BaseModel):
    value_aaa: "InputAAA" = Field(alias="valueAAA")


class InputAAA(BaseModel):
    val: str


class InputAB(BaseModel):
    val: str
    value_a: Optional["InputA"] = Field(alias="valueA", default=None)


class InputE(BaseModel):
    val: EnumE
