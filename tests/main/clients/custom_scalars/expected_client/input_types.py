from datetime import datetime
from typing import Any

from .base_model import BaseModel
from .custom_scalars import Code


class TestInput(BaseModel):
    a: datetime
    b: Code
    c: int
    d: Any


TestInput.model_rebuild()
