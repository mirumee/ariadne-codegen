from typing import Annotated, List, Literal, Union

from pydantic import Field

from .base_model import BaseModel


class ListAnimals(BaseModel):
    list_animals: List[
        Annotated[
            Union[
                "ListAnimalsListAnimalsAnimal",
                "ListAnimalsListAnimalsCat",
                "ListAnimalsListAnimalsDog",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="listAnimals")


class ListAnimalsListAnimalsAnimal(BaseModel):
    typename__: Literal["Animal"] = Field(alias="__typename")
    name: str


class ListAnimalsListAnimalsCat(BaseModel):
    typename__: Literal["Cat"] = Field(alias="__typename")
    name: str
    kittens: int


class ListAnimalsListAnimalsDog(BaseModel):
    typename__: Literal["Dog"] = Field(alias="__typename")
    name: str
    puppies: int


ListAnimals.model_rebuild()
