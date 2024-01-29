from typing import Any, AsyncIterator, Dict, List, Optional, Union

from .async_base_client import AsyncBaseClient
from .custom_scalars import ComplexScalar, SimpleScalar
from .get_animal_by_name import (
    GetAnimalByName,
    GetAnimalByNameAnimalByNameAnimal,
    GetAnimalByNameAnimalByNameCat,
    GetAnimalByNameAnimalByNameDog,
)
from .get_animal_fragment_with_extra import GetAnimalFragmentWithExtra
from .get_authenticated_user import GetAuthenticatedUser, GetAuthenticatedUserMe
from .get_complex_scalar import GetComplexScalar
from .get_simple_scalar import GetSimpleScalar
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
    async def get_authenticated_user(self, **kwargs: Any) -> GetAuthenticatedUserMe:
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
        response = await self.execute(
            query=query,
            operation_name="GetAuthenticatedUser",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetAuthenticatedUser.model_validate(data).me

    async def list_strings_1(self, **kwargs: Any) -> Optional[List[Optional[str]]]:
        query = gql(
            """
            query ListStrings_1 {
              optionalListOptionalString
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="ListStrings_1", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListStrings1.model_validate(data).optional_list_optional_string

    async def list_strings_2(self, **kwargs: Any) -> Optional[List[str]]:
        query = gql(
            """
            query ListStrings_2 {
              optionalListString
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="ListStrings_2", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListStrings2.model_validate(data).optional_list_string

    async def list_strings_3(self, **kwargs: Any) -> List[Optional[str]]:
        query = gql(
            """
            query ListStrings_3 {
              listOptionalString
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="ListStrings_3", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListStrings3.model_validate(data).list_optional_string

    async def list_strings_4(self, **kwargs: Any) -> List[str]:
        query = gql(
            """
            query ListStrings_4 {
              listString
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="ListStrings_4", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListStrings4.model_validate(data).list_string

    async def list_type_a(
        self, **kwargs: Any
    ) -> List[Optional[ListTypeAListOptionalTypeA]]:
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
        response = await self.execute(
            query=query, operation_name="ListTypeA", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListTypeA.model_validate(data).list_optional_type_a

    async def get_animal_by_name(self, name: str, **kwargs: Any) -> Union[
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
        response = await self.execute(
            query=query, operation_name="GetAnimalByName", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetAnimalByName.model_validate(data).animal_by_name

    async def list_animals(self, **kwargs: Any) -> List[
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
        response = await self.execute(
            query=query, operation_name="ListAnimals", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListAnimals.model_validate(data).list_animals

    async def get_animal_fragment_with_extra(
        self, **kwargs: Any
    ) -> GetAnimalFragmentWithExtra:
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
        response = await self.execute(
            query=query,
            operation_name="GetAnimalFragmentWithExtra",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetAnimalFragmentWithExtra.model_validate(data)

    async def get_simple_scalar(self, **kwargs: Any) -> SimpleScalar:
        query = gql(
            """
            query GetSimpleScalar {
              justSimpleScalar
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="GetSimpleScalar", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetSimpleScalar.model_validate(data).just_simple_scalar

    async def get_complex_scalar(self, **kwargs: Any) -> ComplexScalar:
        query = gql(
            """
            query GetComplexScalar {
              justComplexScalar
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="GetComplexScalar",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetComplexScalar.model_validate(data).just_complex_scalar

    async def subscribe_strings(
        self, **kwargs: Any
    ) -> AsyncIterator[Optional[List[str]]]:
        query = gql(
            """
            subscription SubscribeStrings {
              optionalListString
            }
            """
        )
        variables: Dict[str, object] = {}
        async for data in self.execute_ws(
            query=query,
            operation_name="SubscribeStrings",
            variables=variables,
            **kwargs
        ):
            yield SubscribeStrings.model_validate(data).optional_list_string

    async def unwrap_fragment(
        self, **kwargs: Any
    ) -> FragmentWithSingleFieldQueryUnwrapFragment:
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
        response = await self.execute(
            query=query, operation_name="UnwrapFragment", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return UnwrapFragment.model_validate(data).query_unwrap_fragment
