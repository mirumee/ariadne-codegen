from typing import Optional

from .base_model import BaseModel


class UserFilterInput(BaseModel):
    name: Optional[str] = None
    manager: Optional["UserFilterInput"] = None
    tags: Optional[list[str]] = None
