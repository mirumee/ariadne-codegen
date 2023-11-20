from typing import List

from pydantic import Field

from .shorter_results_fragments import ListAnimalsFragment


class GetAnimalFragmentWithExtra(ListAnimalsFragment):
    list_string: List[str] = Field(alias="listString")
