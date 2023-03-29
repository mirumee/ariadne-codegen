from .async_base_client import AsyncBaseClient
from .interface_a import InterfaceA
from .interface_b import InterfaceB
from .interface_c import InterfaceC
from .union_a import UnionA
from .union_b import UnionB
from .union_c import UnionC


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

    async def union_a(self) -> UnionA:
        query = gql(
            """
            query UnionA {
              queryU {
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
        return UnionA.parse_obj(data)

    async def union_b(self) -> UnionB:
        query = gql(
            """
            query UnionB {
              queryU {
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
        return UnionB.parse_obj(data)

    async def union_c(self) -> UnionC:
        query = gql(
            """
            query UnionC {
              queryU {
                __typename
                id
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return UnionC.parse_obj(data)
