from .async_base_client import AsyncBaseClient
from .test import Test


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def test(self) -> Test:
        query = gql(
            """
            query test {
              testQuery
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return Test.parse_obj(data)
