from pydantic import Field

from ..base_model import BaseModel
from ..common_mixins import CommonMixin
from ..mixins_a import MixinA


class GetQueryA(BaseModel):
    query_a: "GetQueryAQueryA" = Field(alias="queryA")


class GetQueryAQueryA(BaseModel, MixinA, CommonMixin):
    field_a: int = Field(alias="fieldA")
