from pydantic import Field

from .base_model import BaseModel


class CMutation(BaseModel):
    const_mutation: int = Field(alias="constMutation")
