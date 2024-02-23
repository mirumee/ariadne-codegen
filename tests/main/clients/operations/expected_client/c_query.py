from pydantic import Field

from .base_model import BaseModel


class CQuery(BaseModel):
    const_query: str = Field(alias="constQuery")


CQuery.model_rebuild()
