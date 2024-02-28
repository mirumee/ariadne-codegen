from typing import Any, Dict

from .async_base_client import AsyncBaseClient
from .example_query_1 import ExampleQuery1
from .example_query_2 import ExampleQuery2
from .example_query_3 import ExampleQuery3


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def example_query_1(self, **kwargs: Any) -> ExampleQuery1:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="exampleQuery1", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return ExampleQuery1.model_validate(_data)

    async def example_query_2(self, **kwargs: Any) -> ExampleQuery2:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="exampleQuery2", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return ExampleQuery2.model_validate(_data)

    async def example_query_3(self, **kwargs: Any) -> ExampleQuery3:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="exampleQuery3", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return ExampleQuery3.model_validate(_data)
