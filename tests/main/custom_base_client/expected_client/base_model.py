from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        allow_population_by_field_name = True
