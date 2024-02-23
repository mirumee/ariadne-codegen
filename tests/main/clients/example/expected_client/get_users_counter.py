from pydantic import Field

from .base_model import BaseModel


class GetUsersCounter(BaseModel):
    users_counter: int = Field(alias="usersCounter")


GetUsersCounter.model_rebuild()
