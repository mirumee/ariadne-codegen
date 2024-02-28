from typing import Any, Dict

from .async_base_client import AsyncBaseClient
from .test import Test


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def test(self, **kwargs: Any) -> Test:
        _query = gql(
            """
            query test {
              testQuery
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="test", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return Test.model_validate(_data)
