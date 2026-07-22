from typing import Optional

from .base_model import BaseModel
from .fragments import (
    UserFields,
    UserFieldsFriends,  # noqa: F401
)


class ListUsersWithManager(BaseModel):
    users: list["ListUsersWithManagerUsers"]


class ListUsersWithManagerUsers(UserFields):
    manager: Optional["ListUsersWithManagerUsersManager"]


class ListUsersWithManagerUsersManager(BaseModel):
    id: str
    name: str
