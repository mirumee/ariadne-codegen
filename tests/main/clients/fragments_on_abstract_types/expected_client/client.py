from typing import Any, Dict

from .async_base_client import AsyncBaseClient
from .query_with_fragment_on_sub_interface import QueryWithFragmentOnSubInterface
from .query_with_fragment_on_sub_interface_with_inline_fragment import (
    QueryWithFragmentOnSubInterfaceWithInlineFragment,
)
from .query_with_fragment_on_union_member import QueryWithFragmentOnUnionMember


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def query_with_fragment_on_sub_interface(
        self, **kwargs: Any
    ) -> QueryWithFragmentOnSubInterface:
        _query = gql(
            """
            query queryWithFragmentOnSubInterface {
              queryInterface {
                __typename
                ...fragmentA
              }
            }

            fragment fragmentA on InterfaceA {
              id
              valueA
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query,
            operation_name="queryWithFragmentOnSubInterface",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return QueryWithFragmentOnSubInterface.model_validate(_data)

    async def query_with_fragment_on_sub_interface_with_inline_fragment(
        self, **kwargs: Any
    ) -> QueryWithFragmentOnSubInterfaceWithInlineFragment:
        _query = gql(
            """
            query queryWithFragmentOnSubInterfaceWithInlineFragment {
              queryInterface {
                __typename
                ...fragmentAWithInlineFragment
              }
            }

            fragment fragmentAWithInlineFragment on InterfaceA {
              id
              valueA
              ... on TypeA {
                another
              }
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query,
            operation_name="queryWithFragmentOnSubInterfaceWithInlineFragment",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return QueryWithFragmentOnSubInterfaceWithInlineFragment.model_validate(_data)

    async def query_with_fragment_on_union_member(
        self, **kwargs: Any
    ) -> QueryWithFragmentOnUnionMember:
        _query = gql(
            """
            query queryWithFragmentOnUnionMember {
              queryUnion {
                __typename
                ...fragmentB
              }
            }

            fragment fragmentB on TypeB {
              id
              valueB
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query,
            operation_name="queryWithFragmentOnUnionMember",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return QueryWithFragmentOnUnionMember.model_validate(_data)
