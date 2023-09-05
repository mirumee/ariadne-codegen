from datetime import datetime
from typing import Annotated, Any

from pydantic import PlainSerializer

from .base_model import BaseModel
from .custom_scalars import Code, serialize_code


class TestInput(BaseModel):
    a: datetime
    b: Annotated[Code, PlainSerializer(serialize_code)]
    c: int
    d: Any


TestInput.model_rebuild()
