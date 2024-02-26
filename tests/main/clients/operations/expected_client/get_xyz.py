from typing import Literal, Union

from pydantic import Field

from .base_model import BaseModel
from .fragments import FragmentY


class GetXYZ(BaseModel):
    xyz: Union["GetXYZXyzTypeX", "GetXYZXyzTypeY", "GetXYZXyzTypeZ"] = Field(
        discriminator="typename__"
    )


class GetXYZXyzTypeX(BaseModel):
    typename__: Literal["TypeX"] = Field(alias="__typename")
    value_x: str = Field(alias="valueX")


class GetXYZXyzTypeY(FragmentY):
    typename__: Literal["TypeY"] = Field(alias="__typename")


class GetXYZXyzTypeZ(BaseModel):
    typename__: Literal["TypeZ"] = Field(alias="__typename")


GetXYZ.model_rebuild()
GetXYZ.model_rebuild()
GetXYZ.model_rebuild()
GetXYZXyzTypeX.model_rebuild()
GetXYZXyzTypeY.model_rebuild()
GetXYZXyzTypeZ.model_rebuild()
