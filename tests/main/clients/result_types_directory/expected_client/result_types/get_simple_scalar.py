from typing import Any

from pydantic import Field

from ..base_model import BaseModel


class GetSimpleScalar(BaseModel):
    just_simple_scalar: Any = Field(alias="justSimpleScalar")
