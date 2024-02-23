from .base_model import BaseModel


class GetD(BaseModel):
    d: str


GetD.model_rebuild()
