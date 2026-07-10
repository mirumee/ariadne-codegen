from .base_model import BaseModel
from .fragments import (
    UserFields,
    UserFieldsFriends,  # noqa: F401
)


class ListUsers(BaseModel):
    users: list["ListUsersUsers"]


class ListUsersUsers(UserFields):
    pass
