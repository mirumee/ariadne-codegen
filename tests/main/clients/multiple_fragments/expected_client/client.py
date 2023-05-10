from .async_base_client import AsyncBaseClient
from .example_query1 import ExampleQuery1
from .example_query2 import ExampleQuery2
from .example_query3 import ExampleQuery3


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def example_query1(self) -> ExampleQuery1:
        query = gql(
            """
            query exampleQuery1 {
              exampleQuery {
                value
                ...MinimalA
              }
            }

            fragment MinimalA on TypeA {
              id
              fieldB {
                ...MinimalB
              }
            }

            fragment MinimalB on TypeB {
              id
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ExampleQuery1.parse_obj(data)

    async def example_query2(self) -> ExampleQuery2:
        query = gql(
            """
            query exampleQuery2 {
              exampleQuery {
                ...FullA
              }
            }

            fragment FullA on TypeA {
              id
              value
              fieldB {
                ...FullB
              }
            }

            fragment FullB on TypeB {
              id
              value
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ExampleQuery2.parse_obj(data)

    async def example_query3(self) -> ExampleQuery3:
        query = gql(
            """
            query exampleQuery3 {
              exampleQuery {
                ...CompleteA
              }
            }

            fragment CompleteA on TypeA {
              id
              value
              fieldB {
                id
                value
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ExampleQuery3.parse_obj(data)
