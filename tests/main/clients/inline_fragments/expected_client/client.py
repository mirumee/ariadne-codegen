from typing import Any, Dict

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
    async def interface_a(self, **kwargs: Any) -> InterfaceA:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="InterfaceA", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return InterfaceA.model_validate(_data)

    async def interface_b(self, **kwargs: Any) -> InterfaceB:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="InterfaceB", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return InterfaceB.model_validate(_data)

    async def interface_c(self, **kwargs: Any) -> InterfaceC:
        _query = gql(
            """
            query InterfaceC {
              queryI {
                __typename
                id
              }
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="InterfaceC", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return InterfaceC.model_validate(_data)

    async def list_interface(self, **kwargs: Any) -> ListInterface:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="ListInterface", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return ListInterface.model_validate(_data)

    async def interface_with_typename(self, **kwargs: Any) -> InterfaceWithTypename:
        _query = gql(
            """
            query InterfaceWithTypename {
              queryI {
                __typename
                id
              }
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query,
            operation_name="InterfaceWithTypename",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return InterfaceWithTypename.model_validate(_data)

    async def union_a(self, **kwargs: Any) -> UnionA:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="UnionA", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return UnionA.model_validate(_data)

    async def union_b(self, **kwargs: Any) -> UnionB:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="UnionB", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return UnionB.model_validate(_data)

    async def list_union(self, **kwargs: Any) -> ListUnion:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="ListUnion", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return ListUnion.model_validate(_data)

    async def query_with_fragment_on_interface(
        self, **kwargs: Any
    ) -> QueryWithFragmentOnInterface:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query,
            operation_name="queryWithFragmentOnInterface",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return QueryWithFragmentOnInterface.model_validate(_data)

    async def query_with_fragment_on_union(
        self, **kwargs: Any
    ) -> QueryWithFragmentOnUnion:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query,
            operation_name="queryWithFragmentOnUnion",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return QueryWithFragmentOnUnion.model_validate(_data)

    async def query_with_fragment_on_query_with_interface(
        self, **kwargs: Any
    ) -> QueryWithFragmentOnQueryWithInterface:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query,
            operation_name="queryWithFragmentOnQueryWithInterface",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return QueryWithFragmentOnQueryWithInterface.model_validate(_data)

    async def query_with_fragment_on_query_with_union(
        self, **kwargs: Any
    ) -> QueryWithFragmentOnQueryWithUnion:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query,
            operation_name="queryWithFragmentOnQueryWithUnion",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return QueryWithFragmentOnQueryWithUnion.model_validate(_data)
