from typing import Any, Optional

from .base_model import BaseModel


class CreateUserInput(BaseModel):
    name: str
    avatar: Optional[Any] = None
