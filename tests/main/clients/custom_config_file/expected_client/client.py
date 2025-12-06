from typing import Any

from .async_base_client import AsyncBaseClient
from .test import Test


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def test(self, **kwargs: Any) -> Test:
        query = gql(
            """
            query test {
              testQuery
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="test", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return Test.model_validate(data)
