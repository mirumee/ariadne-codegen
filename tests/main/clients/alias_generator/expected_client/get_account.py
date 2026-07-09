from typing import Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel


class GetAccount(BaseModel):
    account: Union["GetAccountAccountUser", "GetAccountAccountAdmin"] = Field(
        discriminator="typename__"
    )


class GetAccountAccountUser(BaseModel):
    typename__: Literal["User"] = Field(alias="__typename")
    id: str
    first_name: Optional[str]


class GetAccountAccountAdmin(BaseModel):
    typename__: Literal["Admin"] = Field(alias="__typename")
    id: str
    access_level: int


GetAccount.model_rebuild()
