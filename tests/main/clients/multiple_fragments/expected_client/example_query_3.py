from pydantic import Field

from .base_model import BaseModel
from .fragments import CompleteA


class ExampleQuery3(BaseModel):
    example_query: "ExampleQuery3ExampleQuery" = Field(alias="exampleQuery")


class ExampleQuery3ExampleQuery(CompleteA):
    pass
