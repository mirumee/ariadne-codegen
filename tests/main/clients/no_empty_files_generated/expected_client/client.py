from typing import Any, Optional, Union

from .async_base_client import AsyncBaseClient
from .base_model import UNSET, UnsetType
from .list_all_users import ListAllUsers
from .list_users_by_country import ListUsersByCountry


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def list_all_users(self, **kwargs: Any) -> ListAllUsers:
        query = gql("""
            query ListAllUsers {
              users {
                id
                firstName
                lastName
                email
                location {
                  country
                }
              }
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="ListAllUsers", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListAllUsers.model_validate(data)

    async def list_users_by_country(
        self, country: Union[Optional[str], UnsetType] = UNSET, **kwargs: Any
    ) -> ListUsersByCountry:
        query = gql("""
            query ListUsersByCountry($country: String) {
              users(country: $country) {
                ...BasicUser
                ...UserPersonalData
              }
            }

            fragment BasicUser on User {
              id
              email
            }

            fragment UserPersonalData on User {
              firstName
              lastName
            }
            """)
        variables: dict[str, object] = {"country": country}
        response = await self.execute(
            query=query,
            operation_name="ListUsersByCountry",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return ListUsersByCountry.model_validate(data)
