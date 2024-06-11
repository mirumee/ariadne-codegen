from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import Role


class AddUserInput(BaseModel):
    name: str
    age: Optional[int] = None
    email: Optional[str] = None
    role: Optional[Role] = Role.USER
    created_at: Optional[Any] = Field(alias="createdAt", default=None)


class UpdateUserInput(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    role: Optional[Role] = None
    created_at: Optional[Any] = Field(alias="createdAt", default=None)
