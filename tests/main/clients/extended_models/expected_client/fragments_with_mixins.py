from pydantic import Field

from .base_model import BaseModel
from .common_mixins import CommonMixin
from .fragments import FragmentA, FragmentB


class FragmentsWithMixins(BaseModel):
    query_a: "FragmentsWithMixinsQueryA" = Field(alias="queryA")
    query_b: "FragmentsWithMixinsQueryB" = Field(alias="queryB")


class FragmentsWithMixinsQueryA(FragmentA, CommonMixin):
    pass


class FragmentsWithMixinsQueryB(FragmentB, CommonMixin):
    pass


FragmentsWithMixins.update_forward_refs()
FragmentsWithMixinsQueryA.update_forward_refs()
FragmentsWithMixinsQueryB.update_forward_refs()
