from .base_model import BaseModel
from .enums import EnumF


class GetF(BaseModel):
    f: "GetFF"


class GetFF(BaseModel):
    val: EnumF
