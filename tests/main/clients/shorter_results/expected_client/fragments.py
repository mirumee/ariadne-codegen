from .base_model import BaseModel


class AnimalFragment(BaseModel):
    name: str


AnimalFragment.update_forward_refs()
