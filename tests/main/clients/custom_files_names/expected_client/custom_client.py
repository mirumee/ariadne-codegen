from typing import Dict

from .async_base_client import AsyncBaseClient
from .custom_input_types import inputA
from .get_query_a import GetQueryA


def gql(q: str) -> str:
    return q


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
        variables: Dict[str, object] = {"dataA": data_a}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetQueryA.model_validate(data)
