from pydantic import Field

from .base_model import BaseModel
from .fragments import (
    FullA,
    FullAFieldB,  # noqa: F401
)


class ExampleQuery2(BaseModel):
    example_query: "ExampleQuery2ExampleQuery" = Field(alias="exampleQuery")


class ExampleQuery2ExampleQuery(FullA):
    pass


ExampleQuery2.model_rebuild()
