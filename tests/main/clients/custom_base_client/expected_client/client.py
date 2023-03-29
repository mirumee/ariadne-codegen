from .custom_base_client import CustomAsyncBaseClient
from .get_query_a import GetQueryA
from .input_types import inputA


def gql(q: str) -> str:
    return q


class Client(CustomAsyncBaseClient):
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
        variables: dict[str, object] = {"dataA": data_a}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetQueryA.parse_obj(data)
