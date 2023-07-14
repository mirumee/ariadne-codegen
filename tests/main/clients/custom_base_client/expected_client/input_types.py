from .base_model import BaseModel
from .enums import enumA


class inputA(BaseModel):
    version: enumA


inputA.model_rebuild()
