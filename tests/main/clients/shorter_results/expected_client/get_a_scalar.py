from pydantic import Field

from .base_model import BaseModel
from .scalars import MyScalar_


class GetAScalar(BaseModel):
    just_a_scalar: MyScalar_ = Field(alias="justAScalar")


GetAScalar.model_rebuild()
