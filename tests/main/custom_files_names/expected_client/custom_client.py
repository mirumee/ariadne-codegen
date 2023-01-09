from typing import Optional

from .async_base_client import AsyncBaseClient
from .custom_input_types import inputA
from .get_query_a import GetQueryA

gql = lambda q: q


class Client(AsyncBaseClient):
    async def get_query_a(self, data_a: inputA) -> GetQueryA:
        query = gql(
            """
            query getQueryA($dataA: inputA!) {
              queryA(dataA: $dataA) {
                fieldA
              }
            }
            """
        )
        variables: dict = {"dataA": data_a}
        response = await self.execute(query=query, variables=variables)
        return GetQueryA.parse_obj(response.json().get("data", {}))
