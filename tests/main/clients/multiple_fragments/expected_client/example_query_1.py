from pydantic import Field

from .base_model import BaseModel
from .fragments import (
    MinimalA,
    MinimalAFieldB,  # noqa: F401
)


class ExampleQuery1(BaseModel):
    example_query: "ExampleQuery1ExampleQuery" = Field(alias="exampleQuery")


class ExampleQuery1ExampleQuery(MinimalA):
    value: str


ExampleQuery1.model_rebuild()
