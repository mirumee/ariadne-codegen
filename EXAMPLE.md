# Example

## Schema file

```gql
schema {
  query: Query
  mutation: Mutation
  subscription: Subscription
}

type Query {
  users(country: String): [User!]!
}

type Mutation {
  userCreate(userData: UserCreateInput!): User
  userPreferences(data: UserPreferencesInput): Boolean!
  fileUpload(file: Upload!): Boolean!
}

type Subscription {
  usersCounter: Int!
}

scalar Upload

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
  notificationsPreferences: NotificationsPreferencesInput! = {
    receiveMails: true
    receivePushNotifications: true
    receiveSms: false
    title: "Mr"
  }
}

input NotificationsPreferencesInput {
  receiveMails: Boolean!
  receivePushNotifications: Boolean!
  receiveSms: Boolean!
  title: String!
}
```


## Queries/mutations/subscriptions file

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

subscription GetUsersCounter {
  usersCounter
}

mutation uploadFile($file: Upload!) {
  fileUpload(file: $file)
}
```


## Running

Add `[tool.ariadne-codegen]` section to `pyproject.toml` with paths to files with [schema](#schema-file) and [queries/mutations](#queriesmutations-file).

```toml
[tool.ariadne-codegen]
schema_path = "schema.graphql" 
queries_path = "queries.graphql"
```

Run command to generate code:

```
$ ariadne-codegen
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
    fragments.py
    get_users_counter.py
    input_types.py
    list_all_users.py
    list_users_by_country.py
    scalars.py
    upload_file.py
```

### Client class

Generated client class inherits from `AsyncBaseClient` and has async method for every provided query/mutation.

```py
# graphql_client/client.py

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
        response = await self.execute(
            query=query, operation_name="CreateUser", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return CreateUser.model_validate(data)

    async def list_all_users(self, **kwargs: Any) -> ListAllUsers:
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
        response = await self.execute(
            query=query, operation_name="ListAllUsers", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListAllUsers.model_validate(data)

    async def list_users_by_country(
        self, country: Union[Optional[str], UnsetType] = UNSET, **kwargs: Any
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
        response = await self.execute(
            query=query,
            operation_name="ListUsersByCountry",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return ListUsersByCountry.model_validate(data)

    async def get_users_counter(self, **kwargs: Any) -> AsyncIterator[GetUsersCounter]:
        query = gql(
            """
            subscription GetUsersCounter {
              usersCounter
            }
            """
        )
        variables: Dict[str, object] = {}
        async for data in self.execute_ws(
            query=query, operation_name="GetUsersCounter", variables=variables, **kwargs
        ):
            yield GetUsersCounter.model_validate(data)

    async def upload_file(self, file: Upload, **kwargs: Any) -> UploadFile:
        query = gql(
            """
            mutation uploadFile($file: Upload!) {
              fileUpload(file: $file)
            }
            """
        )
        variables: Dict[str, object] = {"file": file}
        response = await self.execute(
            query=query, operation_name="uploadFile", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return UploadFile.model_validate(data)
```

### Base client

Base client is copied from path provided in `base_client_file_path` and has to contain definition of class with name provided in `base_client_name`.

### Base model

`base_model.py` is a file that contains preconfigured class, which extends pydantic's `BaseModel` class and is used by other generated classes.

### Input types

Models are generated from inputs from provided schema. They are used as arguments types in client`s methods.

```py
# graphql_client/input_types.py

from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import Color


class UserCreateInput(BaseModel):
    first_name: Optional[str] = Field(alias="firstName", default=None)
    last_name: Optional[str] = Field(alias="lastName", default=None)
    email: str
    favourite_color: Optional[Color] = Field(alias="favouriteColor", default=None)
    location: Optional["LocationInput"] = None


class LocationInput(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None


class UserPreferencesInput(BaseModel):
    lucky_number: Optional[int] = Field(alias="luckyNumber", default=7)
    favourite_word: Optional[str] = Field(alias="favouriteWord", default="word")
    color_opacity: Optional[float] = Field(alias="colorOpacity", default=1.0)
    excluded_tags: Optional[List[str]] = Field(
        alias="excludedTags", default_factory=lambda: ["offtop", "tag123"]
    )
    notifications_preferences: "NotificationsPreferencesInput" = Field(
        alias="notificationsPreferences",
        default_factory=lambda: globals()[
            "NotificationsPreferencesInput"
        ].model_validate(
            {
                "receiveMails": True,
                "receivePushNotifications": True,
                "receiveSms": False,
                "title": "Mr",
            }
        ),
    )


class NotificationsPreferencesInput(BaseModel):
    receive_mails: bool = Field(alias="receiveMails")
    receive_push_notifications: bool = Field(alias="receivePushNotifications")
    receive_sms: bool = Field(alias="receiveSms")
    title: str
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

### Query/mutation/subscription types

For every provided query/mutation/subscription there is a generated file that contains models which correspond to return type of operation. File name is generated by converting operation name to snake case. Root models has the same name as query/mutation/subscription, and depend classes use it as prefix in their names.

```py
# graphql_client/create_user.py

from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class CreateUser(BaseModel):
    user_create: Optional["CreateUserUserCreate"] = Field(alias="userCreate")


class CreateUserUserCreate(BaseModel):
    id: str
```

```py
# graphql_client/list_all_users.py

from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class ListAllUsers(BaseModel):
    users: List["ListAllUsersUsers"]


class ListAllUsersUsers(BaseModel):
    id: str
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
    email: str
    location: Optional["ListAllUsersUsersLocation"]


class ListAllUsersUsersLocation(BaseModel):
    country: Optional[str]
```

```py
# graphql_client/list_users_by_country.py

from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import Color
from .fragments import BasicUser, UserPersonalData


class ListUsersByCountry(BaseModel):
    users: List["ListUsersByCountryUsers"]


class ListUsersByCountryUsers(BasicUser, UserPersonalData):
    favourite_color: Optional[Color] = Field(alias="favouriteColor")
```

```py
# graphql_client/get_users_counter.py

from pydantic import Field

from .base_model import BaseModel


class GetUsersCounter(BaseModel):
    users_counter: int = Field(alias="usersCounter")
```

```py
# graphql_client/upload_file.py

from pydantic import Field

from .base_model import BaseModel


class UploadFile(BaseModel):
    file_upload: bool = Field(alias="fileUpload")
```

### Fragments file

This file contains classes generated from all fragments used in any provided operation.

```py
# graphql_client/fragments.py

from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class BasicUser(BaseModel):
    id: str
    email: str


class UserPersonalData(BaseModel):
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
```

### Init file

Generated init file contains reimports and list of all generated classes.

```py
# graphql_client/__init__.py

from .async_base_client import AsyncBaseClient
from .base_model import BaseModel, Upload
from .client import Client
from .create_user import CreateUser, CreateUserUserCreate
from .enums import Color
from .exceptions import (
    GraphQLClientError,
    GraphQLClientGraphQLError,
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQLClientInvalidResponseError,
)
from .fragments import BasicUser, UserPersonalData
from .get_users_counter import GetUsersCounter
from .input_types import (
    LocationInput,
    NotificationsPreferencesInput,
    UserCreateInput,
    UserPreferencesInput,
)
from .list_all_users import ListAllUsers, ListAllUsersUsers, ListAllUsersUsersLocation
from .list_users_by_country import ListUsersByCountry, ListUsersByCountryUsers
from .upload_file import UploadFile

__all__ = [
    "AsyncBaseClient",
    "BaseModel",
    "BasicUser",
    "Client",
    "Color",
    "CreateUser",
    "CreateUserUserCreate",
    "GetUsersCounter",
    "GraphQLClientError",
    "GraphQLClientGraphQLError",
    "GraphQLClientGraphQLMultiError",
    "GraphQLClientHttpError",
    "GraphQLClientInvalidResponseError",
    "ListAllUsers",
    "ListAllUsersUsers",
    "ListAllUsersUsersLocation",
    "ListUsersByCountry",
    "ListUsersByCountryUsers",
    "LocationInput",
    "NotificationsPreferencesInput",
    "Upload",
    "UploadFile",
    "UserCreateInput",
    "UserPersonalData",
    "UserPreferencesInput",
]
```
