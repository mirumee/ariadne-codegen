from typing import List

from pydantic import Field

from .no_global_imports_fragments import ListAnimalsFragment


class GetAnimalFragmentWithExtra(ListAnimalsFragment):
    list_string: List[str] = Field(alias="listString")
