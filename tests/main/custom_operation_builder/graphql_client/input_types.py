from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import Role


class AddUserInput(BaseModel):
    name: str
    age: int
    email: str
    role: Role
    created_at: str = Field(alias="createdAt")


class UpdateUserInput(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    role: Optional[Role] = None
    created_at: Optional[str] = Field(alias="createdAt", default=None)
