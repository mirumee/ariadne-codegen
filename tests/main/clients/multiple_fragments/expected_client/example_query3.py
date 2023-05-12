from pydantic import Field

from .base_model import BaseModel
from .fragments import CompleteA


class ExampleQuery3(BaseModel):
    example_query: "ExampleQuery3ExampleQuery" = Field(alias="exampleQuery")


class ExampleQuery3ExampleQuery(CompleteA):
    pass


ExampleQuery3.update_forward_refs()
ExampleQuery3ExampleQuery.update_forward_refs()
