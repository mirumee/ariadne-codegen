from pydantic import Field

from ..base_model import BaseModel


class SubscribeToTypeA(BaseModel):
    subscribe_to_type_a: "SubscribeToTypeASubscribeToTypeA" = Field(
        alias="subscribeToTypeA"
    )


class SubscribeToTypeASubscribeToTypeA(BaseModel):
    field_a: int = Field(alias="fieldA")
