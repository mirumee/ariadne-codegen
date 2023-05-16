from typing import Union

from pydantic import Field

from .base_model import BaseModel


class GetAnimalByName(BaseModel):
    animal_by_name: Union[
        "GetAnimalByNameAnimalByNameAnimal",
        "GetAnimalByNameAnimalByNameCat",
        "GetAnimalByNameAnimalByNameDog",
    ] = Field(alias="animalByName")


class GetAnimalByNameAnimalByNameAnimal(BaseModel):
    __typename__: str = Field(alias="__typename")
    name: str


class GetAnimalByNameAnimalByNameCat(BaseModel):
    __typename__: str = Field(alias="__typename")
    name: str
    kittens: int


class GetAnimalByNameAnimalByNameDog(BaseModel):
    __typename__: str = Field(alias="__typename")
    name: str
    puppies: int


GetAnimalByName.update_forward_refs()
GetAnimalByNameAnimalByNameAnimal.update_forward_refs()
GetAnimalByNameAnimalByNameCat.update_forward_refs()
GetAnimalByNameAnimalByNameDog.update_forward_refs()
