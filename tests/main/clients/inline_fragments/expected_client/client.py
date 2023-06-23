from .async_base_client import AsyncBaseClient
from .interface_a import InterfaceA
from .interface_b import InterfaceB
from .interface_c import InterfaceC
from .interface_with_typename import InterfaceWithTypename
from .list_interface import ListInterface
from .list_union import ListUnion
from .query_with_fragment_on_interface import QueryWithFragmentOnInterface
from .query_with_fragment_on_query_with_interface import (
    QueryWithFragmentOnQueryWithInterface,
)
from .query_with_fragment_on_query_with_union import QueryWithFragmentOnQueryWithUnion
from .query_with_fragment_on_union import QueryWithFragmentOnUnion
from .union_a import UnionA
from .union_b import UnionB


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def interface_a(self) -> InterfaceA:
        query = gql(
            """
            query InterfaceA {
              queryI {
                __typename
                id
                ... on TypeA {
                  fieldA
                }
                ... on TypeB {
                  fieldB
                }
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return InterfaceA.parse_obj(data)

    async def interface_b(self) -> InterfaceB:
        query = gql(
            """
            query InterfaceB {
              queryI {
                __typename
                id
                ... on TypeA {
                  fieldA
                }
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return InterfaceB.parse_obj(data)

    async def interface_c(self) -> InterfaceC:
        query = gql(
            """
            query InterfaceC {
              queryI {
                id
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return InterfaceC.parse_obj(data)

    async def list_interface(self) -> ListInterface:
        query = gql(
            """
            query ListInterface {
              queryListI {
                __typename
                id
                ... on TypeA {
                  fieldA
                }
                ... on TypeB {
                  fieldB
                }
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListInterface.parse_obj(data)

    async def interface_with_typename(self) -> InterfaceWithTypename:
        query = gql(
            """
            query InterfaceWithTypename {
              queryI {
                __typename
                id
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return InterfaceWithTypename.parse_obj(data)

    async def union_a(self) -> UnionA:
        query = gql(
            """
            query UnionA {
              queryU {
                __typename
                ... on TypeA {
                  id
                  fieldA
                }
                ... on TypeB {
                  id
                  fieldB
                }
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return UnionA.parse_obj(data)

    async def union_b(self) -> UnionB:
        query = gql(
            """
            query UnionB {
              queryU {
                __typename
                ... on TypeA {
                  id
                  fieldA
                }
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return UnionB.parse_obj(data)

    async def list_union(self) -> ListUnion:
        query = gql(
            """
            query ListUnion {
              queryListU {
                __typename
                ... on TypeA {
                  id
                  fieldA
                }
                ... on TypeB {
                  id
                  fieldB
                }
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListUnion.parse_obj(data)

    async def query_with_fragment_on_interface(self) -> QueryWithFragmentOnInterface:
        query = gql(
            """
            query queryWithFragmentOnInterface {
              queryI {
                __typename
                ...fragmentOnInterface
              }
            }

            fragment fragmentOnInterface on Interface {
              id
              ... on TypeA {
                fieldA
              }
              ... on TypeB {
                fieldB
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return QueryWithFragmentOnInterface.parse_obj(data)

    async def query_with_fragment_on_union(self) -> QueryWithFragmentOnUnion:
        query = gql(
            """
            query queryWithFragmentOnUnion {
              queryU {
                __typename
                ...fragmentOnUnion
              }
            }

            fragment fragmentOnUnion on Union {
              ... on TypeA {
                id
                fieldA
              }
              ... on TypeB {
                id
                fieldB
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return QueryWithFragmentOnUnion.parse_obj(data)

    async def query_with_fragment_on_query_with_interface(
        self,
    ) -> QueryWithFragmentOnQueryWithInterface:
        query = gql(
            """
            query queryWithFragmentOnQueryWithInterface {
              ...FragmentOnQueryWithInterface
            }

            fragment FragmentOnQueryWithInterface on Query {
              queryI {
                id
                ... on TypeA {
                  fieldA
                }
                ... on TypeB {
                  fieldB
                }
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return QueryWithFragmentOnQueryWithInterface.parse_obj(data)

    async def query_with_fragment_on_query_with_union(
        self,
    ) -> QueryWithFragmentOnQueryWithUnion:
        query = gql(
            """
            query queryWithFragmentOnQueryWithUnion {
              ...FragmentOnQueryWithUnion
            }

            fragment FragmentOnQueryWithUnion on Query {
              queryU {
                ... on TypeA {
                  id
                  fieldA
                }
                ... on TypeB {
                  id
                  fieldB
                }
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return QueryWithFragmentOnQueryWithUnion.parse_obj(data)
