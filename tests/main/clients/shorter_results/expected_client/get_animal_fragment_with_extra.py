from pydantic import Field

from .shorter_results_fragments import (
    ListAnimalsFragment,
    ListAnimalsFragmentListAnimals,  # noqa: F401
)


class GetAnimalFragmentWithExtra(ListAnimalsFragment):
    list_string: list[str] = Field(alias="listString")
