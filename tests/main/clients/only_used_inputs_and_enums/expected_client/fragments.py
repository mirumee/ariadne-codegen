from .base_model import BaseModel
from .enums import EnumG, EnumGG


class FragmentG(BaseModel):
    val: EnumG


class FragmentGG(BaseModel):
    val: EnumGG


FragmentG.model_rebuild()
FragmentGG.model_rebuild()
