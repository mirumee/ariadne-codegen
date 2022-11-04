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
}

input UserCreateInput {
  firstName: String
  lastName: String
  email: String!
  favourite_color: Color 
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
  favourite_color: Color 
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
```


## Queries/mutations file

```gql
mutation CreateUser($user_data: UserCreateInput!) {
    userCreate(userData: $user_data) {
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
        id
        email
        favourite_color
    }
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
    base_client.py
    client.py
    create_user.py
    enums.py
    input_types.py
    list_all_users.py
    list_users_by_country.py
    schema_types.py
```

### Client class

Generated client class inherits from `BaseClient` and has async method for every provided query/mutation.

```py
# graphql_client/client.py

from typing import Optional

from .base_client import BaseClient
from .create_user import CreateUser
from .input_types import UserCreateInput
from .list_all_users import ListAllUsers
from .list_users_by_country import ListUsersByCountry

gql = lambda q: q


class Client(BaseClient):
    async def create_user(self, user_data: UserCreateInput) -> CreateUser:
        query = gql(
            """
            mutation CreateUser($user_data: UserCreateInput!) {
              userCreate(userData: $user_data) {
                id
              }
            }
            """
        )
        variables: dict = {"user_data": user_data}
        response = await self.execute(query=query, variables=variables)
        return CreateUser.parse_obj(response.json().get("data", {}))

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
        return ListAllUsers.parse_obj(response.json().get("data", {}))

    async def list_users_by_country(self, country: str) -> ListUsersByCountry:
        query = gql(
            """
            query ListUsersByCountry($country: String!) {
              users(country: $country) {
                id
                email
                favourite_color
              }
            }
            """
        )
        variables: dict = {"country": country}
        response = await self.execute(query=query, variables=variables)
        return ListUsersByCountry.parse_obj(response.json().get("data", {}))
```

### Base client

Base client is copied from path provided in `base_client_file_path` and has to contain definition of class with name provided in `base_client_name`.

### Input types

Models are generated from inputs from provided schema. They are used as arguments types in client`s methods.

```py
# graphql_client/input_types.py

from typing import Optional

from pydantic import BaseModel

from .enums import Color


class UserCreateInput(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    email: str
    favourite_color: Optional["Color"]
    location: Optional["LocationInput"]


class LocationInput(BaseModel):
    city: Optional[str]
    country: Optional[str]


UserCreateInput.update_forward_refs()
LocationInput.update_forward_refs()
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

### Schema types

Models are generated from types from provided schema. Query/mutation specific models are generated based on these classes.

```py
# graphql_client/schema_types.py

from typing import Optional

from pydantic import BaseModel

from .enums import Color


class User(BaseModel):
    id: str
    firstName: Optional[str]
    lastName: Optional[str]
    email: str
    favourite_color: Optional["Color"]
    location: Optional["Location"]


class Location(BaseModel):
    city: Optional[str]
    country: Optional[str]


User.update_forward_refs()
Location.update_forward_refs()
```

### Query/mutation types

For every provided query/mutation there is generated file, that contains models which correspond to return type of operation. File name is generated by converting query/mutation name to snake case. Root models has the same name as query/mutation, and depend classes use it as prefix in their names.

```py
# graphql_client/create_user.py

from typing import Optional

from pydantic import BaseModel


class CreateUser(BaseModel):
    userCreate: Optional["CreateUserUser"]


class CreateUserUser(BaseModel):
    id: str


CreateUser.update_forward_refs()
CreateUserUser.update_forward_refs()
```

```py
# graphql_client/list_all_users.py

from typing import Optional

from pydantic import BaseModel


class ListAllUsers(BaseModel):
    users: list["ListAllUsersUser"]


class ListAllUsersUser(BaseModel):
    id: str
    firstName: Optional[str]
    lastName: Optional[str]
    email: str
    location: Optional["ListAllUsersLocation"]


class ListAllUsersLocation(BaseModel):
    country: Optional[str]


ListAllUsers.update_forward_refs()
ListAllUsersUser.update_forward_refs()
ListAllUsersLocation.update_forward_refs()
```

```py
# graphql_client/list_users_by_country.py

from typing import Optional

from pydantic import BaseModel

from .enums import Color


class ListUsersByCountry(BaseModel):
    users: list["ListUsersByCountryUser"]


class ListUsersByCountryUser(BaseModel):
    id: str
    email: str
    favourite_color: Optional["Color"]


ListUsersByCountry.update_forward_refs()
ListUsersByCountryUser.update_forward_refs()
```

### Init file

Generated init file contains reimports and list of all generated classes.

```py
# graphql_client/__init__.py

from .base_client import BaseClient
from .client import Client
from .create_user import CreateUser, CreateUserUser
from .enums import Color
from .input_types import LocationInput, UserCreateInput
from .list_all_users import ListAllUsers, ListAllUsersLocation, ListAllUsersUser
from .list_users_by_country import ListUsersByCountry, ListUsersByCountryUser
from .schema_types import Location, User

__all__ = [
    "BaseClient",
    "Client",
    "Color",
    "CreateUser",
    "CreateUserUser",
    "ListAllUsers",
    "ListAllUsersLocation",
    "ListAllUsersUser",
    "ListUsersByCountry",
    "ListUsersByCountryUser",
    "Location",
    "LocationInput",
    "User",
    "UserCreateInput",
]
```
