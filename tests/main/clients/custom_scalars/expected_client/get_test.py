from typing import Any

from pydantic import Field

from .base_model import BaseModel
from .scalars import CODE, CUSTOMID, DATETIME


class GetTest(BaseModel):
    test_query: "GetTestTestQuery" = Field(alias="testQuery")


class GetTestTestQuery(BaseModel):
    date: DATETIME
    code: CODE
    id: CUSTOMID
    other: Any


GetTest.model_rebuild()
GetTestTestQuery.model_rebuild()
