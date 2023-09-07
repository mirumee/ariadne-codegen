from datetime import datetime
from typing import Annotated, Any

from pydantic import BeforeValidator, Field

from .base_model import BaseModel
from .custom_scalars import Code, parse_code


class GetTest(BaseModel):
    test_query: "GetTestTestQuery" = Field(alias="testQuery")


class GetTestTestQuery(BaseModel):
    date: datetime
    code: Annotated[Code, BeforeValidator(parse_code)]
    id: int
    other: Any


GetTest.model_rebuild()
GetTestTestQuery.model_rebuild()
