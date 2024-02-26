from typing import Literal, Union

from pydantic import Field

from .base_model import BaseModel


class GetAnimalByName(BaseModel):
    animal_by_name: Union[
        "GetAnimalByNameAnimalByNameAnimal",
        "GetAnimalByNameAnimalByNameCat",
        "GetAnimalByNameAnimalByNameDog",
    ] = Field(alias="animalByName", discriminator="typename__")


class GetAnimalByNameAnimalByNameAnimal(BaseModel):
    typename__: Literal["Animal"] = Field(alias="__typename")
    name: str


class GetAnimalByNameAnimalByNameCat(BaseModel):
    typename__: Literal["Cat"] = Field(alias="__typename")
    name: str
    kittens: int


class GetAnimalByNameAnimalByNameDog(BaseModel):
    typename__: Literal["Dog"] = Field(alias="__typename")
    name: str
    puppies: int


GetAnimalByName.model_rebuild()
GetAnimalByName.model_rebuild()
GetAnimalByName.model_rebuild()
GetAnimalByNameAnimalByNameAnimal.model_rebuild()
GetAnimalByNameAnimalByNameCat.model_rebuild()
GetAnimalByNameAnimalByNameDog.model_rebuild()
