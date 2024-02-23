from .base_model import BaseModel


class GetA2(BaseModel):
    a: str


GetA2.model_rebuild()
