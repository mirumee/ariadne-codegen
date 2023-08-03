from typing import Any

from .base_model import BaseModel
from .scalars import CODE, CUSTOMID, DATETIME


class TestInput(BaseModel):
    a: DATETIME
    b: CODE
    c: CUSTOMID
    d: Any


TestInput.model_rebuild()
