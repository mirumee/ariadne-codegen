from .base_model import BaseModel
from .enums import enumA


class inputA(BaseModel):
    version: enumA


inputA.update_forward_refs()
