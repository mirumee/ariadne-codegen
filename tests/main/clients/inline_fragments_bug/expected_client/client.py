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