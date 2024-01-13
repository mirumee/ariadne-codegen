from pydantic import Field

from ..base_model import BaseModel
from ..common_mixins import CommonMixin
from ..fragments import FragmentA, FragmentB


class GetQueryWithMixinsFragments(BaseModel):
    query_a: "GetQueryWithMixinsFragmentsQueryA" = Field(alias="queryA")
    query_b: "GetQueryWithMixinsFragmentsQueryB" = Field(alias="queryB")


class GetQueryWithMixinsFragmentsQueryA(FragmentA, CommonMixin):
    pass


class GetQueryWithMixinsFragmentsQueryB(FragmentB, CommonMixin):
    pass
