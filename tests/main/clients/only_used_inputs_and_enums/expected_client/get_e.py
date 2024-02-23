from .base_model import BaseModel


class GetE(BaseModel):
    e: str


GetE.model_rebuild()
