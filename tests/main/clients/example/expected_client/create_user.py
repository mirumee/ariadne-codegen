from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class CreateUser(BaseModel):
    user_create: Optional["CreateUserUserCreate"] = Field(alias="userCreate")


class CreateUserUserCreate(BaseModel):
    id: str


CreateUser.model_rebuild()
