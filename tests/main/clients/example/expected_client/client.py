from typing import Any, AsyncIterator, Dict, Optional, Union

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
    async def create_user(
        self, user_data: UserCreateInput, **kwargs: Any
    ) -> CreateUser:
        _query = gql(
            """
            mutation CreateUser($userData: UserCreateInput!) {
              userCreate(userData: $userData) {
                id
              }
            }
            """
        )
        _variables: Dict[str, object] = {"userData": user_data}
        _response = await self.execute(
            query=_query, operation_name="CreateUser", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return CreateUser.model_validate(_data)

    async def list_all_users(self, **kwargs: Any) -> ListAllUsers:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="ListAllUsers", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return ListAllUsers.model_validate(_data)

    async def list_users_by_country(
        self, country: Union[Optional[str], UnsetType] = UNSET, **kwargs: Any
    ) -> ListUsersByCountry:
        _query = gql(
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
        _variables: Dict[str, object] = {"country": country}
        _response = await self.execute(
            query=_query,
            operation_name="ListUsersByCountry",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return ListUsersByCountry.model_validate(_data)

    async def get_users_counter(self, **kwargs: Any) -> AsyncIterator[GetUsersCounter]:
        _query = gql(
            """
            subscription GetUsersCounter {
              usersCounter
            }
            """
        )
        _variables: Dict[str, object] = {}
        async for _data in self.execute_ws(
            query=_query,
            operation_name="GetUsersCounter",
            variables=_variables,
            **kwargs
        ):
            yield GetUsersCounter.model_validate(_data)

    async def upload_file(self, file: Upload, **kwargs: Any) -> UploadFile:
        _query = gql(
            """
            mutation uploadFile($file: Upload!) {
              fileUpload(file: $file)
            }
            """
        )
        _variables: Dict[str, object] = {"file": file}
        _response = await self.execute(
            query=_query, operation_name="uploadFile", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return UploadFile.model_validate(_data)
