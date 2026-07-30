from .base_model import BaseModel
from .fragments import BasicUser, UserPersonalData


class ListUsersByCountry(BaseModel):
    users: list["ListUsersByCountryUsers"]


class ListUsersByCountryUsers(BasicUser, UserPersonalData):
    pass


ListUsersByCountry.model_rebuild()
