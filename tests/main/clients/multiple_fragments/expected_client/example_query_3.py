from pydantic import Field

from .base_model import BaseModel
from .fragments import CompleteA


class ExampleQuery3(BaseModel):
    example_query: "ExampleQuery3ExampleQuery" = Field(alias="exampleQuery")


ExampleQuery3ExampleQuery = CompleteA
ExampleQuery3.model_rebuild()
