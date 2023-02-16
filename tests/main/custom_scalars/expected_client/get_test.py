from datetime import datetime
from typing import Any

from pydantic import Field

from .base_model import BaseModel
from .custom_scalars import Code


class GetTest(BaseModel):
    test_query: "GetTestTestQuery" = Field(alias="testQuery")


class GetTestTestQuery(BaseModel):
    date: datetime
    code: Code
    id: str
    other: Any


GetTest.update_forward_refs()
GetTestTestQuery.update_forward_refs()
