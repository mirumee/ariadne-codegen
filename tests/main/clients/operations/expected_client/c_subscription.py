from pydantic import Field

from .base_model import BaseModel


class CSubscription(BaseModel):
    const_subscription: float = Field(alias="constSubscription")


CSubscription.model_rebuild()
