from typing import List

from pydantic import Field

from .fragments import AnimalFragment


class GetAnimalFragmentWithExtra(AnimalFragment):
    list_string: List[str] = Field(alias="listString")


GetAnimalFragmentWithExtra.update_forward_refs()
