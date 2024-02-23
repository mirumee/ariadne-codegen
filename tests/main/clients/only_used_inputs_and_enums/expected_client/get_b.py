from .base_model import BaseModel


class GetB(BaseModel):
    b: str


GetB.model_rebuild()
