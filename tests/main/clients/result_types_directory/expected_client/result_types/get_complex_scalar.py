from typing import Any

from pydantic import Field

from ..base_model import BaseModel


class GetComplexScalar(BaseModel):
    just_complex_scalar: Any = Field(alias="justComplexScalar")
