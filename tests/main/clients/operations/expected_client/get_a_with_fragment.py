from pydantic import Field

from .base_model import BaseModel
from .fragments import FragmentB


class GetAWithFragment(BaseModel):
    a: "GetAWithFragmentA"


class GetAWithFragmentA(BaseModel):
    value: str
    value_b: "GetAWithFragmentAValueB" = Field(alias="valueB")


class GetAWithFragmentAValueB(FragmentB):
    pass


GetAWithFragment.model_rebuild()
GetAWithFragmentA.model_rebuild()
