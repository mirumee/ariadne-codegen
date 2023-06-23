from typing import List

from pydantic import Field

from .base_model import BaseModel


class ListAnimalsFragment(BaseModel):
    list_animals: List["ListAnimalsFragmentListAnimals"] = Field(alias="listAnimals")


class ListAnimalsFragmentListAnimals(BaseModel):
    name: str


ListAnimalsFragment.update_forward_refs()
ListAnimalsFragmentListAnimals.update_forward_refs()
