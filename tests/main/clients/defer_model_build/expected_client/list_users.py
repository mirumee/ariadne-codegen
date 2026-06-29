from .base_model import BaseModel
from .fragments import UserFields


class ListUsers(BaseModel):
    users: list["ListUsersUsers"]


class ListUsersUsers(UserFields):
    pass
