from typing import AsyncIterator, Dict, List, Optional, Union

from .async_base_client import AsyncBaseClient
from .custom_scalars import MyScalar
from .get_a_scalar import GetAScalar
from .get_animal_by_name import (
    GetAnimalByName,
    GetAnimalByNameAnimalByNameAnimal,
    GetAnimalByNameAnimalByNameCat,
    GetAnimalByNameAnimalByNameDog,
)
from .get_animal_fragment_with_extra import GetAnimalFragmentWithExtra
from .get_authenticated_user import GetAuthenticatedUser, GetAuthenticatedUserMe
from .list_animals import (
    ListAnimals,
    ListAnimalsListAnimalsAnimal,
    ListAnimalsListAnimalsCat,
    ListAnimalsListAnimalsDog,
)
from .list_strings_1 import ListStrings1
from .list_strings_2 import ListStrings2
from .list_strings_3 import ListStrings3
from .list_strings_4 import ListStrings4
from .list_type_a import ListTypeA, ListTypeAListOptionalTypeA
from .shorter_results_fragments import FragmentWithSingleFieldQueryUnwrapFragment
from .subscribe_strings import SubscribeStrings
from .unwrap_fragment import UnwrapFragment


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
        variables: Dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetAuthenticatedUser.model_validate(data).me

    async def list_strings_1(self) -> Optional[List[Optional[str]]]:
        query = gql(
            """
            query ListStrings_1 {
              optionalListOptionalString
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListStrings1.model_validate(data).optional_list_optional_string

    async def list_strings_2(self) -> Optional[List[str]]:
        query = gql(
            """
            query ListStrings_2 {
              optionalListString
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListStrings2.model_validate(data).optional_list_string

    async def list_strings_3(self) -> List[Optional[str]]:
        query = gql(
            """
            query ListStrings_3 {
              listOptionalString
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListStrings3.model_validate(data).list_optional_string

    async def list_strings_4(self) -> List[str]:
        query = gql(
            """
            query ListStrings_4 {
              listString
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListStrings4.model_validate(data).list_string

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
        variables: Dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListTypeA.model_validate(data).list_optional_type_a

    async def get_animal_by_name(
        self, name: str
    ) -> Union[
        GetAnimalByNameAnimalByNameAnimal,
        GetAnimalByNameAnimalByNameCat,
        GetAnimalByNameAnimalByNameDog,
    ]:
        query = gql(
            """
            query GetAnimalByName($name: String!) {
              animalByName(name: $name) {
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
        variables: Dict[str, object] = {"name": name}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetAnimalByName.model_validate(data).animal_by_name

    async def list_animals(
        self,
    ) -> List[
        Union[
            ListAnimalsListAnimalsAnimal,
            ListAnimalsListAnimalsCat,
            ListAnimalsListAnimalsDog,
        ]
    ]:
        query = gql(
            """
            query ListAnimals {
              listAnimals {
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
        variables: Dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListAnimals.model_validate(data).list_animals

    async def get_animal_fragment_with_extra(self) -> GetAnimalFragmentWithExtra:
        query = gql(
            """
            query GetAnimalFragmentWithExtra {
              ...ListAnimalsFragment
              listString
            }

            fragment ListAnimalsFragment on Query {
              listAnimals {
                name
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetAnimalFragmentWithExtra.model_validate(data)

    async def get_a_scalar(self) -> MyScalar:
        query = gql(
            """
            query GetAScalar {
              justAScalar
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetAScalar.model_validate(data).just_a_scalar

    async def subscribe_strings(self) -> AsyncIterator[Optional[List[str]]]:
        query = gql(
            """
            subscription SubscribeStrings {
              optionalListString
            }
            """
        )
        variables: Dict[str, object] = {}
        async for data in self.execute_ws(query=query, variables=variables):
            yield SubscribeStrings.model_validate(data).optional_list_string

    async def unwrap_fragment(self) -> FragmentWithSingleFieldQueryUnwrapFragment:
        query = gql(
            """
            query UnwrapFragment {
              ...FragmentWithSingleField
            }

            fragment FragmentWithSingleField on Query {
              queryUnwrapFragment {
                id
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return UnwrapFragment.model_validate(data).query_unwrap_fragment
