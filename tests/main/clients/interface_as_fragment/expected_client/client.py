from typing import Any, Dict

from .async_base_client import AsyncBaseClient
from .my_mutation import MyMutation


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def my_mutation(self, id: str, **kwargs: Any) -> MyMutation:
        query = gql(
            """
            mutation my_mutation($id: ID!) {
              change_item(id: $id) {
                contacts {
                  ...Item
                }
                errors {
                  __typename
                  ... on ItemError {
                    ...ItemError
                  }
                }
              }
            }

            fragment Item on Item {
              id
            }

            fragment ItemError on ItemError {
              __typename
              message
            }
            """
        )
        variables: Dict[str, object] = {"id": id}
        response = await self.execute(
            query=query, operation_name="my_mutation", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return MyMutation.model_validate(data)
