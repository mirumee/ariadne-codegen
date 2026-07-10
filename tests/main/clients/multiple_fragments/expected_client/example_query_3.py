from pydantic import Field

from .base_model import BaseModel
from .fragments import (
    CompleteA,
    CompleteAFieldB,  # noqa: F401
)


class ExampleQuery3(BaseModel):
    example_query: "ExampleQuery3ExampleQuery" = Field(alias="exampleQuery")


class ExampleQuery3ExampleQuery(CompleteA):
    pass


ExampleQuery3.model_rebuild()
