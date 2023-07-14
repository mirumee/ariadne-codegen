from pydantic import Field

from .base_model import BaseModel
from .custom_scalars import MyScalar


class GetAScalar(BaseModel):
    just_a_scalar: MyScalar = Field(alias="justAScalar")


GetAScalar.model_rebuild()
