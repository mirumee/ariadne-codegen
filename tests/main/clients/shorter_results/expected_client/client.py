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
        _query = gql(
            """
            query GetAuthenticatedUser {
              me {
                id
                username
              }
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query,
            operation_name="GetAuthenticatedUser",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return GetAuthenticatedUser.model_validate(_data).me

    async def list_strings_1(self, **kwargs: Any) -> Optional[List[Optional[str]]]:
        _query = gql(
            """
            query ListStrings_1 {
              optionalListOptionalString
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="ListStrings_1", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return ListStrings1.model_validate(_data).optional_list_optional_string

    async def list_strings_2(self, **kwargs: Any) -> Optional[List[str]]:
        _query = gql(
            """
            query ListStrings_2 {
              optionalListString
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="ListStrings_2", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return ListStrings2.model_validate(_data).optional_list_string

    async def list_strings_3(self, **kwargs: Any) -> List[Optional[str]]:
        _query = gql(
            """
            query ListStrings_3 {
              listOptionalString
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="ListStrings_3", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return ListStrings3.model_validate(_data).list_optional_string

    async def list_strings_4(self, **kwargs: Any) -> List[str]:
        _query = gql(
            """
            query ListStrings_4 {
              listString
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="ListStrings_4", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return ListStrings4.model_validate(_data).list_string

    async def list_type_a(
        self, **kwargs: Any
    ) -> List[Optional[ListTypeAListOptionalTypeA]]:
        _query = gql(
            """
            query ListTypeA {
              listOptionalTypeA {
                id
              }
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="ListTypeA", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return ListTypeA.model_validate(_data).list_optional_type_a

    async def get_animal_by_name(self, name: str, **kwargs: Any) -> Union[
        GetAnimalByNameAnimalByNameAnimal,
        GetAnimalByNameAnimalByNameCat,
        GetAnimalByNameAnimalByNameDog,
    ]:
        _query = gql(
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
        _variables: Dict[str, object] = {"name": name}
        _response = await self.execute(
            query=_query,
            operation_name="GetAnimalByName",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return GetAnimalByName.model_validate(_data).animal_by_name

    async def list_animals(self, **kwargs: Any) -> List[
        Union[
            ListAnimalsListAnimalsAnimal,
            ListAnimalsListAnimalsCat,
            ListAnimalsListAnimalsDog,
        ]
    ]:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="ListAnimals", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return ListAnimals.model_validate(_data).list_animals

    async def get_animal_fragment_with_extra(
        self, **kwargs: Any
    ) -> GetAnimalFragmentWithExtra:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query,
            operation_name="GetAnimalFragmentWithExtra",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return GetAnimalFragmentWithExtra.model_validate(_data)

    async def get_simple_scalar(self, **kwargs: Any) -> SimpleScalar:
        _query = gql(
            """
            query GetSimpleScalar {
              justSimpleScalar
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query,
            operation_name="GetSimpleScalar",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return GetSimpleScalar.model_validate(_data).just_simple_scalar

    async def get_complex_scalar(self, **kwargs: Any) -> ComplexScalar:
        _query = gql(
            """
            query GetComplexScalar {
              justComplexScalar
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query,
            operation_name="GetComplexScalar",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return GetComplexScalar.model_validate(_data).just_complex_scalar

    async def subscribe_strings(
        self, **kwargs: Any
    ) -> AsyncIterator[Optional[List[str]]]:
        _query = gql(
            """
            subscription SubscribeStrings {
              optionalListString
            }
            """
        )
        _variables: Dict[str, object] = {}
        async for _data in self.execute_ws(
            query=_query,
            operation_name="SubscribeStrings",
            variables=_variables,
            **kwargs
        ):
            yield SubscribeStrings.model_validate(_data).optional_list_string

    async def unwrap_fragment(
        self, **kwargs: Any
    ) -> FragmentWithSingleFieldQueryUnwrapFragment:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query,
            operation_name="UnwrapFragment",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return UnwrapFragment.model_validate(_data).query_unwrap_fragment
