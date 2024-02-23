from typing import Annotated

from pydantic import BeforeValidator, Field

from .base_model import BaseModel
from .custom_scalars import ComplexScalar, parse_complex_scalar


class GetComplexScalar(BaseModel):
    just_complex_scalar: Annotated[
        ComplexScalar, BeforeValidator(parse_complex_scalar)
    ] = Field(alias="justComplexScalar")


GetComplexScalar.model_rebuild()
