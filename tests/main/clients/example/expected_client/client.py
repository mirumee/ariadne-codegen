from typing import AsyncIterator, Dict, Optional, Union

from .async_base_client import AsyncBaseClient
from .base_model import UNSET, UnsetType, Upload
from .create_user import CreateUser
from .get_users_counter import GetUsersCounter
from .input_types import UserCreateInput
from .list_all_users import ListAllUsers
from .list_users_by_country import ListUsersByCountry
from .upload_file import UploadFile


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def create_user(self, user_data: UserCreateInput) -> CreateUser:
        query = gql(
            """
            mutation CreateUser($userData: UserCreateInput!) {
              userCreate(userData: $userData) {
                id
              }
            }
            """
        )
        variables: Dict[str, object] = {"userData": user_data}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return CreateUser.model_validate(data)

    async def list_all_users(self) -> ListAllUsers:
        query = gql(
            """
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
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListAllUsers.model_validate(data)

    async def list_users_by_country(
        self, country: Union[Optional[str], UnsetType] = UNSET
    ) -> ListUsersByCountry:
        query = gql(
            """
            query ListUsersByCountry($country: String) {
              users(country: $country) {
                ...BasicUser
                ...UserPersonalData
                favouriteColor
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
            """
        )
        variables: Dict[str, object] = {"country": country}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListUsersByCountry.model_validate(data)

    async def get_users_counter(self) -> AsyncIterator[GetUsersCounter]:
        query = gql(
            """
            subscription GetUsersCounter {
              usersCounter
            }
            """
        )
        variables: Dict[str, object] = {}
        async for data in self.execute_ws(query=query, variables=variables):
            yield GetUsersCounter.model_validate(data)

    async def upload_file(self, file: Upload) -> UploadFile:
        query = gql(
            """
            mutation uploadFile($file: Upload!) {
              fileUpload(file: $file)
            }
            """
        )
        variables: Dict[str, object] = {"file": file}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return UploadFile.model_validate(data)
