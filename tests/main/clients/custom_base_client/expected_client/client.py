from typing import Any, Dict

from .custom_base_client import CustomAsyncBaseClient
from .get_query_a import GetQueryA
from .input_types import inputA


def gql(q: str) -> str:
    return q


class Client(CustomAsyncBaseClient):
    async def get_query_a(self, data_a: inputA, **kwargs: Any) -> GetQueryA:
        _query = gql(
            """
            query getQueryA($dataA: inputA!) {
              queryA(dataA: $dataA) {
                fieldA
              }
            }
            """
        )
        _variables: Dict[str, object] = {"dataA": data_a}
        _response = await self.execute(
            query=_query, operation_name="getQueryA", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return GetQueryA.model_validate(_data)
