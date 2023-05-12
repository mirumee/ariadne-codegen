from typing import List, Optional

from .async_base_client import AsyncBaseClient
from .get_authenticated_user import GetAuthenticatedUser, GetAuthenticatedUserMe
from .list_strings_1 import ListStrings1
from .list_strings_2 import ListStrings2
from .list_strings_3 import ListStrings3
from .list_strings_4 import ListStrings4
from .list_type_a import ListTypeA, ListTypeAListOptionalTypeA


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def get_authenticated_user(self) -> GetAuthenticatedUserMe:
        query = gql(
            """
            query GetAuthenticatedUser {
              me {
                id
                username
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetAuthenticatedUser.parse_obj(data).me

    async def list_strings_1(self) -> Optional[List[Optional[str]]]:
        query = gql(
            """
            query ListStrings_1 {
              optionalListOptionalString
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListStrings1.parse_obj(data).optional_list_optional_string

    async def list_strings_2(self) -> Optional[List[str]]:
        query = gql(
            """
            query ListStrings_2 {
              optionalListString
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListStrings2.parse_obj(data).optional_list_string

    async def list_strings_3(self) -> List[Optional[str]]:
        query = gql(
            """
            query ListStrings_3 {
              listOptionalString
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListStrings3.parse_obj(data).list_optional_string

    async def list_strings_4(self) -> List[str]:
        query = gql(
            """
            query ListStrings_4 {
              listString
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListStrings4.parse_obj(data).list_string

    async def list_type_a(self) -> List[Optional[ListTypeAListOptionalTypeA]]:
        query = gql(
            """
            query ListTypeA {
              listOptionalTypeA {
                id
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListTypeA.parse_obj(data).list_optional_type_a
