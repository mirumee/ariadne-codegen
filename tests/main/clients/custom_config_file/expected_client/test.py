from pydantic import Field

from .base_model import BaseModel


class Test(BaseModel):
    test_query: str = Field(alias="testQuery")


Test.update_forward_refs()
