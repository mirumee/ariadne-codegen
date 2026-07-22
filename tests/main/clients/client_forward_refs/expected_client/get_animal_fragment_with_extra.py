from pydantic import Field

from .client_forward_refs_fragments import (
    ListAnimalsFragment,
    ListAnimalsFragmentListAnimals,  # noqa: F401
)


class GetAnimalFragmentWithExtra(ListAnimalsFragment):
    list_string: list[str] = Field(alias="listString")
