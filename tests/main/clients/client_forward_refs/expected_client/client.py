from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any

from .async_base_client import AsyncBaseClient

if TYPE_CHECKING:
    from .get_animal_by_name import GetAnimalByName
    from .get_animal_fragment_with_extra import GetAnimalFragmentWithExtra
    from .get_authenticated_user import GetAuthenticatedUser
    from .get_complex_scalar import GetComplexScalar
    from .get_simple_scalar import GetSimpleScalar
    from .list_animals import ListAnimals
    from .list_strings_1 import ListStrings1
    from .list_strings_2 import ListStrings2
    from .list_strings_3 import ListStrings3
    from .list_strings_4 import ListStrings4
    from .list_type_a import ListTypeA
    from .subscribe_strings import SubscribeStrings
    from .unwrap_fragment import UnwrapFragment


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def get_authenticated_user(self, **kwargs: Any) -> "GetAuthenticatedUser":
        from .get_authenticated_user import GetAuthenticatedUser

        query = gql("""
            query GetAuthenticatedUser {
              me {
                id
                username
              }
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="GetAuthenticatedUser",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetAuthenticatedUser.model_validate(data)

    async def list_strings_1(self, **kwargs: Any) -> "ListStrings1":
        from .list_strings_1 import ListStrings1

        query = gql("""
            query ListStrings_1 {
              optionalListOptionalString
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="ListStrings_1", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListStrings1.model_validate(data)

    async def list_strings_2(self, **kwargs: Any) -> "ListStrings2":
        from .list_strings_2 import ListStrings2

        query = gql("""
            query ListStrings_2 {
              optionalListString
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="ListStrings_2", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListStrings2.model_validate(data)

    async def list_strings_3(self, **kwargs: Any) -> "ListStrings3":
        from .list_strings_3 import ListStrings3

        query = gql("""
            query ListStrings_3 {
              listOptionalString
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="ListStrings_3", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListStrings3.model_validate(data)

    async def list_strings_4(self, **kwargs: Any) -> "ListStrings4":
        from .list_strings_4 import ListStrings4

        query = gql("""
            query ListStrings_4 {
              listString
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="ListStrings_4", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListStrings4.model_validate(data)

    async def list_type_a(self, **kwargs: Any) -> "ListTypeA":
        from .list_type_a import ListTypeA

        query = gql("""
            query ListTypeA {
              listOptionalTypeA {
                id
              }
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="ListTypeA", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListTypeA.model_validate(data)

    async def get_animal_by_name(self, name: str, **kwargs: Any) -> "GetAnimalByName":
        from .get_animal_by_name import GetAnimalByName

        query = gql("""
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
            """)
        variables: dict[str, object] = {"name": name}
        response = await self.execute(
            query=query, operation_name="GetAnimalByName", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetAnimalByName.model_validate(data)

    async def list_animals(self, **kwargs: Any) -> "ListAnimals":
        from .list_animals import ListAnimals

        query = gql("""
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
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="ListAnimals", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListAnimals.model_validate(data)

    async def get_animal_fragment_with_extra(
        self, **kwargs: Any
    ) -> "GetAnimalFragmentWithExtra":
        from .get_animal_fragment_with_extra import GetAnimalFragmentWithExtra

        query = gql("""
            query GetAnimalFragmentWithExtra {
              ...ListAnimalsFragment
              listString
            }

            fragment ListAnimalsFragment on Query {
              listAnimals {
                name
              }
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="GetAnimalFragmentWithExtra",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetAnimalFragmentWithExtra.model_validate(data)

    async def get_simple_scalar(self, **kwargs: Any) -> "GetSimpleScalar":
        from .get_simple_scalar import GetSimpleScalar

        query = gql("""
            query GetSimpleScalar {
              justSimpleScalar
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="GetSimpleScalar", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetSimpleScalar.model_validate(data)

    async def get_complex_scalar(self, **kwargs: Any) -> "GetComplexScalar":
        from .get_complex_scalar import GetComplexScalar

        query = gql("""
            query GetComplexScalar {
              justComplexScalar
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="GetComplexScalar",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetComplexScalar.model_validate(data)

    async def subscribe_strings(
        self, **kwargs: Any
    ) -> AsyncIterator["SubscribeStrings"]:
        from .subscribe_strings import SubscribeStrings

        query = gql("""
            subscription SubscribeStrings {
              optionalListString
            }
            """)
        variables: dict[str, object] = {}
        async for data in self.execute_ws(
            query=query,
            operation_name="SubscribeStrings",
            variables=variables,
            **kwargs
        ):
            yield SubscribeStrings.model_validate(data)

    async def unwrap_fragment(self, **kwargs: Any) -> "UnwrapFragment":
        from .unwrap_fragment import UnwrapFragment

        query = gql("""
            query UnwrapFragment {
              ...FragmentWithSingleField
            }

            fragment FragmentWithSingleField on Query {
              queryUnwrapFragment {
                id
              }
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="UnwrapFragment", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return UnwrapFragment.model_validate(data)
