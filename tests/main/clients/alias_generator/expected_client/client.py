from typing import Any, Optional, Union

from .async_base_client import AsyncBaseClient
from .base_model import UNSET, UnsetType
from .get_account import GetAccount
from .input_types import UserFilter
from .list_users import ListUsers


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def list_users(
        self, filter_: Union[Optional[UserFilter], UnsetType] = UNSET, **kwargs: Any
    ) -> ListUsers:
        query = gql("""
            query ListUsers($filter: UserFilter) {
              users(filter: $filter) {
                id
                firstName
                lastName
                some_field
                productID
                URL
              }
            }
            """)
        variables: dict[str, object] = {"filter": filter_}
        response = await self.execute(
            query=query, operation_name="ListUsers", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListUsers.model_validate(data)

    async def get_account(self, **kwargs: Any) -> GetAccount:
        query = gql("""
            query GetAccount {
              account {
                __typename
                ... on User {
                  id
                  firstName
                }
                ... on Admin {
                  id
                  accessLevel
                }
              }
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="GetAccount", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetAccount.model_validate(data)
