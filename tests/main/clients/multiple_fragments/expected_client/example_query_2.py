from pydantic import Field

from .base_model import BaseModel
from .fragments import FullA


class ExampleQuery2(BaseModel):
    example_query: "ExampleQuery2ExampleQuery" = Field(alias="exampleQuery")


ExampleQuery2ExampleQuery = FullA
ExampleQuery2.model_rebuild()
