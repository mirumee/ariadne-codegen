from typing import Any, List, Optional

from .async_base_client import AsyncBaseClient
from .get_query_a import GetQueryA
from .get_query_b import GetQueryB


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def get_query_a(self) -> GetQueryA:
        query = gql(
            """
            query getQueryA {
              queryA @mixin(from: ".mixins_a", import: "MixinA") @mixin(from: ".common_mixins", import: "CommonMixin") {
                fieldA
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetQueryA.parse_obj(data)

    async def get_query_b(self) -> GetQueryB:
        query = gql(
            """
            query getQueryB {
              queryB @mixin(from: ".mixins_b", import: "MixinB") @mixin(from: ".common_mixins", import: "CommonMixin") {
                fieldB
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetQueryB.parse_obj(data)
