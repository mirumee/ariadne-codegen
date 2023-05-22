from typing import AsyncIterator, List, Optional, Union

from .async_base_client import AsyncBaseClient
from .custom_scalars import MyScalar
from .get_a_scalar import GetAScalar
from .get_animal_by_name import (
    GetAnimalByName,
    GetAnimalByNameAnimalByNameAnimal,
    GetAnimalByNameAnimalByNameCat,
    GetAnimalByNameAnimalByNameDog,
)
from .get_animal_fragment import GetAnimalFragment
from .get_animal_fragment_with_extra import GetAnimalFragmentWithExtra
from .get_authenticated_user import GetAuthenticatedUser, GetAuthenticatedUserMe
from .list_strings_1 import ListStrings1
from .list_strings_2 import ListStrings2
from .list_strings_3 import ListStrings3
from .list_strings_4 import ListStrings4
from .list_type_a import ListTypeA, ListTypeAListOptionalTypeA
from .subscribe_strings import SubscribeStrings


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def get_authenticated_user(self) -> GetAuthenticatedUserMe:
        query = gql(
            """
            query GetAuthenticatedUser {
              me {
                id
                username
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetAuthenticatedUser.parse_obj(data).me

    async def list_strings_1(self) -> Optional[List[Optional[str]]]:
        query = gql(
            """
            query ListStrings_1 {
              optionalListOptionalString
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListStrings1.parse_obj(data).optional_list_optional_string

    async def list_strings_2(self) -> Optional[List[str]]:
        query = gql(
            """
            query ListStrings_2 {
              optionalListString
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListStrings2.parse_obj(data).optional_list_string

    async def list_strings_3(self) -> List[Optional[str]]:
        query = gql(
            """
            query ListStrings_3 {
              listOptionalString
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListStrings3.parse_obj(data).list_optional_string

    async def list_strings_4(self) -> List[str]:
        query = gql(
            """
            query ListStrings_4 {
              listString
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListStrings4.parse_obj(data).list_string

    async def list_type_a(self) -> List[Optional[ListTypeAListOptionalTypeA]]:
        query = gql(
            """
            query ListTypeA {
              listOptionalTypeA {
                id
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListTypeA.parse_obj(data).list_optional_type_a

    async def get_animal_by_name(
        self,
    ) -> Union[
        GetAnimalByNameAnimalByNameAnimal,
        GetAnimalByNameAnimalByNameCat,
        GetAnimalByNameAnimalByNameDog,
    ]:
        query = gql(
            """
            query GetAnimalByName {
              animalByName {
                __typename
                name
                ... on Cat {
                  kittens
                }
                ... on Dog {
                  puppies
                }
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetAnimalByName.parse_obj(data).animal_by_name

    async def get_animal_fragment(self) -> str:
        query = gql(
            """
            query GetAnimalFragment {
              ...AnimalFragment
            }

            fragment AnimalFragment on Animal {
              name
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetAnimalFragment.parse_obj(data).name

    async def get_animal_fragment_with_extra(self) -> GetAnimalFragmentWithExtra:
        query = gql(
            """
            query GetAnimalFragmentWithExtra {
              ...AnimalFragment
              listString
            }

            fragment AnimalFragment on Animal {
              name
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetAnimalFragmentWithExtra.parse_obj(data)

    async def get_a_scalar(self) -> MyScalar:
        query = gql(
            """
            query GetAScalar {
              justAScalar
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetAScalar.parse_obj(data).just_a_scalar

    async def subscribe_strings(self) -> AsyncIterator[Optional[List[str]]]:
        query = gql(
            """
            subscription SubscribeStrings {
              optionalListString
            }
            """
        )
        variables: dict[str, object] = {}
        async for data in self.execute_ws(query=query, variables=variables):
            yield SubscribeStrings.parse_obj(data).optional_list_string
