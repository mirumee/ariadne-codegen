from typing import Any, Dict

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ModelField, validator

from .scalars import SCALARS_PARSE_FUNCTIONS, SCALARS_SERIALIZE_FUNCTIONS


class BaseModel(PydanticBaseModel):
    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
        arbitrary_types_allowed = True

    # pylint: disable=no-self-argument
    @validator("*", pre=True)
    def decode_custom_scalars(cls, value: Any, field: ModelField) -> Any:
        decode = SCALARS_PARSE_FUNCTIONS.get(field.type_)
        if decode and callable(decode):
            return decode(value)
        return value

    def dict(self, **kwargs) -> Dict[str, Any]:
        dict_ = super().dict(**kwargs)
        for key, value in dict_.items():
            serialize = SCALARS_SERIALIZE_FUNCTIONS.get(type(value))
            if serialize and callable(serialize):
                dict_[key] = serialize(value)
        return dict_
