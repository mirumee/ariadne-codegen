from .base_model import BaseModel
from .fragments import FragmentG


class GetG(BaseModel):
    g: "GetGG"


GetGG = FragmentG
GetG.model_rebuild()
