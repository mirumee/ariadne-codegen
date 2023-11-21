from .base_model import BaseModel


class GetAuthenticatedUser(BaseModel):
    me: "GetAuthenticatedUserMe"


class GetAuthenticatedUserMe(BaseModel):
    id: str
    username: str
