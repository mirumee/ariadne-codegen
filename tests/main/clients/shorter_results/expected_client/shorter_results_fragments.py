from typing import List

from pydantic import Field

from .base_model import BaseModel


class FragmentWithSingleField(BaseModel):
    query_unwrap_fragment: "FragmentWithSingleFieldQueryUnwrapFragment" = Field(
        alias="queryUnwrapFragment"
    )


class FragmentWithSingleFieldQueryUnwrapFragment(BaseModel):
    id: int


class ListAnimalsFragment(BaseModel):
    list_animals: List["ListAnimalsFragmentListAnimals"] = Field(alias="listAnimals")


class ListAnimalsFragmentListAnimals(BaseModel):
    name: str


FragmentWithSingleField.model_rebuild()
FragmentWithSingleFieldQueryUnwrapFragment.model_rebuild()
ListAnimalsFragment.model_rebuild()
ListAnimalsFragmentListAnimals.model_rebuild()
