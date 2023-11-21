from pydantic import Field

from .base_model import BaseModel
from .common_mixins import CommonMixin
from .mixins_b import MixinB


class GetQueryB(BaseModel):
    query_b: "GetQueryBQueryB" = Field(alias="queryB")


class GetQueryBQueryB(BaseModel, MixinB, CommonMixin):
    field_b: str = Field(alias="fieldB")
