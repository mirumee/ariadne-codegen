from .base_model import BaseModel


class GetS(BaseModel):
    s: "GetSS"


class GetSS(BaseModel):
    id: int


GetS.model_rebuild()
GetSS.model_rebuild()
