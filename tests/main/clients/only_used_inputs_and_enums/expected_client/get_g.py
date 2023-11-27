from .base_model import BaseModel
from .fragments import FragmentG


class GetG(BaseModel):
    g: "GetGG"


class GetGG(FragmentG):
    pass
