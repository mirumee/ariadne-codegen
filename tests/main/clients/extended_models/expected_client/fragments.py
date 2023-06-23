from pydantic import Field

from .base_model import BaseModel
from .common_mixins import CommonMixin
from .mixins_a import MixinA
from .mixins_b import MixinB


class FragmentA(BaseModel, MixinA):
    field_a: int = Field(alias="fieldA")


class FragmentB(BaseModel, MixinB):
    field_b: str = Field(alias="fieldB")


class GetQueryAFragment(BaseModel):
    query_a: "GetQueryAFragmentQueryA" = Field(alias="queryA")


class GetQueryAFragmentQueryA(BaseModel, MixinA, CommonMixin):
    field_a: int = Field(alias="fieldA")


FragmentA.update_forward_refs()
FragmentB.update_forward_refs()
GetQueryAFragment.update_forward_refs()
GetQueryAFragmentQueryA.update_forward_refs()
