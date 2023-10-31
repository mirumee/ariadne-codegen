from datetime import datetime
from typing import Annotated, Any

from pydantic import BeforeValidator, Field

from .base_model import BaseModel
from .custom_scalars import Code, parse_code


class GetA(BaseModel):
    test_query: "GetATestQuery" = Field(alias="testQuery")


class GetATestQuery(BaseModel):
    date: datetime
    code: Annotated[Code, BeforeValidator(parse_code)]
    id: int
    other: Any


GetA.model_rebuild()
GetATestQuery.model_rebuild()
