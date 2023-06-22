from pydantic import Field

from .base_model import BaseModel
from .common_mixins import CommonMixin
from .mixins_a import MixinA


class GetQueryAFragment(BaseModel):
    query_a: "GetQueryAFragmentQueryA" = Field(alias="queryA")


class GetQueryAFragmentQueryA(BaseModel, MixinA, CommonMixin):
    field_a: int = Field(alias="fieldA")


GetQueryAFragment.update_forward_refs()
GetQueryAFragmentQueryA.update_forward_refs()
