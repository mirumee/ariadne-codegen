# Example

## Schema file

```gql
schema {
  query: Query
  mutation: Mutation
}

type Query {
  users(country: String): [User!]!
}

type Mutation {
  userCreate(userData: UserCreateInput!): User
  userPreferences(data: UserPreferencesInput): Boolean!
}

input UserCreateInput {
  firstName: String
  lastName: String
  email: String!
  favouriteColor: Color 
  location: LocationInput
}

input LocationInput {
  city: String
  country: String
}

type User {
  id: ID!
  firstName: String
  lastName: String
  email: String!
  favouriteColor: Color 
  location: Location
}

type Location {
  city: String
  country: String
}

enum Color {
  BLACK
  WHITE
  RED
  GREEN
  BLUE
  YELLOW
}

input UserPreferencesInput {
  luckyNumber: Int = 7
  favouriteWord: String = "word"
  colorOpacity: Float = 1.0
  excludedTags: [String!] = ["offtop", "tag123"]
  notificationsPreferences: NotificationsPreferencesInput! = {receiveMails: true, receivePushNotifications: true, receiveSms: false, title: "Mr"}
}

input NotificationsPreferencesInput {
  receiveMails: Boolean!
  receivePushNotifications: Boolean!
  receiveSms: Boolean!
  title: String!
}
```


## Queries/mutations file

```gql
mutation CreateUser($userData: UserCreateInput!) {
    userCreate(userData: $userData) {
        id
    }
}

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

query ListUsersByCountry($country: String!) {
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
```


## Running

Add `[graphql-sdk-gen]` section to `pyproject.toml` with paths to files with [schema](#schema-file) and [queries/mutations](#queriesmutations-file).

```toml
[graphql-sdk-gen]
schema_path = "schema.graphql" 
queries_path = "queries.graphql"
```

Run command to generate code.

```
graphql-sdk-gen
```


## Result

### Generated files

Structure of generated package:

```
grapql_client/
    __init__.py
    async_base_client.py
    base_model.py
    client.py
    create_user.py
    enums.py
    exceptions.py
    input_types.py
    list_all_users.py
    list_users_by_country.py
```

### Client class

Generated client class inherits from `AsyncBaseClient` and has async method for every provided query/mutation.

```py
# graphql_client/client.py

from typing import Optional

from .async_base_client import AsyncBaseClient
from .create_user import CreateUser
from .input_types import UserCreateInput
from .list_all_users import ListAllUsers
from .list_users_by_country import ListUsersByCountry

gql = lambda q: q


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
        variables: dict = {"userData": user_data}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return CreateUser.parse_obj(data)

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
        variables: dict = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListAllUsers.parse_obj(data)

    async def list_users_by_country(self, country: str) -> ListUsersByCountry:
        query = gql(
            """
            query ListUsersByCountry($country: String!) {
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
        variables: dict = {"country": country}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return ListUsersByCountry.parse_obj(data)
```

### Base client

Base client is copied from path provided in `base_client_file_path` and has to contain definition of class with name provided in `base_client_name`.

### Base model

`base_model.py` is a file that contains preconfigured class, which extends pydantic's `BaseModel` class and is used by other generated classes.

### Input types

Models are generated from inputs from provided schema. They are used as arguments types in client`s methods.

```py
# graphql_client/input_types.py

from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import Color


class LocationInput(BaseModel):
    city: Optional[str]
    country: Optional[str]


class UserCreateInput(BaseModel):
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
    email: str
    favourite_color: Optional[Color] = Field(alias="favouriteColor")
    location: Optional["LocationInput"]


class NotificationsPreferencesInput(BaseModel):
    receive_mails: bool = Field(alias="receiveMails")
    receive_push_notifications: bool = Field(alias="receivePushNotifications")
    receive_sms: bool = Field(alias="receiveSms")
    title: str


class UserPreferencesInput(BaseModel):
    lucky_number: Optional[int] = Field(alias="luckyNumber", default=7)
    favourite_word: Optional[str] = Field(alias="favouriteWord", default="word")
    color_opacity: Optional[float] = Field(alias="colorOpacity", default=1.0)
    excluded_tags: Optional[list[str]] = Field(
        alias="excludedTags", default_factory=lambda: ["offtop", "tag123"]
    )
    notifications_preferences: "NotificationsPreferencesInput" = Field(
        alias="notificationsPreferences",
        default=NotificationsPreferencesInput.parse_obj(
            {
                "receiveMails": True,
                "receivePushNotifications": True,
                "receiveSms": False,
                "title": "Mr",
            }
        ),
    )


LocationInput.update_forward_refs()
UserCreateInput.update_forward_refs()
NotificationsPreferencesInput.update_forward_refs()
UserPreferencesInput.update_forward_refs()
```

### Enums

Enums are generated from enums from provided schema. They are used in other generated classes as field types, but also as arguments types in client`s methods.

```py
# graphql_client/enums.py

from enum import Enum


class Color(str, Enum):
    BLACK = "BLACK"
    WHITE = "WHITE"
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    YELLOW = "YELLOW"
```

### Query/mutation types

For every provided query/mutation there is generated file, that contains models which correspond to return type of operation. File name is generated by converting query/mutation name to snake case. Root models has the same name as query/mutation, and depend classes use it as prefix in their names.

```py
# graphql_client/create_user.py

from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class CreateUser(BaseModel):
    user_create: Optional["CreateUserUserCreate"] = Field(alias="userCreate")


class CreateUserUserCreate(BaseModel):
    id: str


CreateUser.update_forward_refs()
CreateUserUserCreate.update_forward_refs()
```

```py
# graphql_client/list_all_users.py

from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class ListAllUsers(BaseModel):
    users: list["ListAllUsersUsers"]


class ListAllUsersUsers(BaseModel):
    id: str
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
    email: str
    location: Optional["ListAllUsersUsersLocation"]


class ListAllUsersUsersLocation(BaseModel):
    country: Optional[str]


ListAllUsers.update_forward_refs()
ListAllUsersUsers.update_forward_refs()
ListAllUsersUsersLocation.update_forward_refs()
```

```py
# graphql_client/list_users_by_country.py

from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import Color


class ListUsersByCountry(BaseModel):
    users: list["ListUsersByCountryUsers"]


class ListUsersByCountryUsers(BaseModel):
    id: str
    email: str
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
    favourite_color: Optional[Color] = Field(alias="favouriteColor")


ListUsersByCountry.update_forward_refs()
ListUsersByCountryUsers.update_forward_refs()
```

### Init file

Generated init file contains reimports and list of all generated classes.

```py
# graphql_client/__init__.py

from .async_base_client import AsyncBaseClient
from .base_model import BaseModel
from .client import Client
from .create_user import CreateUser, CreateUserUserCreate
from .enums import Color
from .exceptions import (
    GraphQLClientError,
    GraphQLClientGraphQLError,
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQlClientInvalidResponseError,
)
from .input_types import (
    LocationInput,
    NotificationsPreferencesInput,
    UserCreateInput,
    UserPreferencesInput,
)
from .list_all_users import ListAllUsers, ListAllUsersUsers, ListAllUsersUsersLocation
from .list_users_by_country import ListUsersByCountry, ListUsersByCountryUsers

__all__ = [
    "AsyncBaseClient",
    "BaseModel",
    "Client",
    "Color",
    "CreateUser",
    "CreateUserUserCreate",
    "GraphQLClientError",
    "GraphQLClientGraphQLError",
    "GraphQLClientGraphQLMultiError",
    "GraphQLClientHttpError",
    "GraphQlClientInvalidResponseError",
    "ListAllUsers",
    "ListAllUsersUsers",
    "ListAllUsersUsersLocation",
    "ListUsersByCountry",
    "ListUsersByCountryUsers",
    "LocationInput",
    "NotificationsPreferencesInput",
    "UserCreateInput",
    "UserPreferencesInput",
]
```
