from typing import Any, Optional, Union

from .async_base_client import AsyncBaseClient
from .base_model import UNSET, UnsetType
from .get_user import GetUser
from .input_types import UserFilterInput
from .list_users import ListUsers
from .list_users_with_manager import ListUsersWithManager


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def get_user(self, id: str, **kwargs: Any) -> GetUser:
        query = gql("""
            query GetUser($id: ID!) {
              user(id: $id) {
                id
                name
                friends {
                  id
                  name
                }
              }
            }
            """)
        variables: dict[str, object] = {"id": id}
        response = await self.execute(
            query=query, operation_name="GetUser", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetUser.model_validate(data)

    async def list_users(
        self,
        filter_: Union[Optional[UserFilterInput], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> ListUsers:
        query = gql("""
            query ListUsers($filter: UserFilterInput) {
              users(filter: $filter) {
                ...UserFields
              }
            }

            fragment UserFields on User {
              id
              name
              friends {
                id
                name
              }
            }
            """)
        variables: dict[str, object] = {"filter": filter_}
        response = await self.execute(
            query=query, operation_name="ListUsers", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListUsers.model_validate(data)

    async def list_users_with_manager(
        self,
        filter_: Union[Optional[UserFilterInput], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> ListUsersWithManager:
        query = gql("""
            query ListUsersWithManager($filter: UserFilterInput) {
              users(filter: $filter) {
                ...UserFields
                manager {
                  id
                  name
                }
              }
            }

            fragment UserFields on User {
              id
              name
              friends {
                id
                name
              }
            }
            """)
        variables: dict[str, object] = {"filter": filter_}
        response = await self.execute(
            query=query,
            operation_name="ListUsersWithManager",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return ListUsersWithManager.model_validate(data)
