from pydantic import Field

from .base_model import BaseModel
from .custom_scalars import SimpleScalar


class GetSimpleScalar(BaseModel):
    just_simple_scalar: SimpleScalar = Field(alias="justSimpleScalar")


GetSimpleScalar.model_rebuild()
