from .base_model import BaseModel
from .custom_enums import enumA


class inputA(BaseModel):
    version: enumA


inputA.model_rebuild()
