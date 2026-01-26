from typing import Any

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
        query = gql("""
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
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="queryWithFragmentOnSubInterface",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return QueryWithFragmentOnSubInterface.model_validate(data)

    async def query_with_fragment_on_sub_interface_with_inline_fragment(
        self, **kwargs: Any
    ) -> QueryWithFragmentOnSubInterfaceWithInlineFragment:
        query = gql("""
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
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="queryWithFragmentOnSubInterfaceWithInlineFragment",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return QueryWithFragmentOnSubInterfaceWithInlineFragment.model_validate(data)

    async def query_with_fragment_on_union_member(
        self, **kwargs: Any
    ) -> QueryWithFragmentOnUnionMember:
        query = gql("""
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
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="queryWithFragmentOnUnionMember",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return QueryWithFragmentOnUnionMember.model_validate(data)
