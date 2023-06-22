from typing import List

from pydantic import Field

from .fragments import ListAnimalsFragment


class GetAnimalFragmentWithExtra(ListAnimalsFragment):
    list_string: List[str] = Field(alias="listString")


GetAnimalFragmentWithExtra.update_forward_refs()
