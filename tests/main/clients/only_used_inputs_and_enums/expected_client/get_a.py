from .base_model import BaseModel


class GetA(BaseModel):
    a: str


GetA.model_rebuild()
