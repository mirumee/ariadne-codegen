from typing import List, Literal

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
    typename__: Literal["Animal", "Cat", "Dog"] = Field(alias="__typename")
    name: str


FragmentWithSingleField.model_rebuild()
FragmentWithSingleFieldQueryUnwrapFragment.model_rebuild()
ListAnimalsFragment.model_rebuild()
ListAnimalsFragmentListAnimals.model_rebuild()
