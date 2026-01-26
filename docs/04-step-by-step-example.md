---
title: Step-by-step example
---

# Step-by-Step example

This example shows how **ariadne-codegen** can take a GraphQL schema and a set of queries, generate a fully typed Python client, and produce ready-to-use models for queries, mutations, and subscriptions.

## Schema file

We start with a GraphQL schema that defines queries, mutations, and subscriptions.
This schema includes `User` types, input objects for creating users and setting preferences, and a `Color` enum. It also shows how to use default values in input objects.

```graphql
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

Next we define the operations we want to use: a mutation to create a user, queries to fetch all users or filter them by country, a subscription to count users in real time, and a mutation to upload a file.
Notice that we also define fragments (`BasicUser` and `UserPersonalData`) to reuse fields across queries.

```graphql
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

To generate Python code, add a `[tool.ariadne-codegen]` section to your `pyproject.toml` with paths to the schema and queries files.

```toml
[tool.ariadne-codegen]
schema_path = "schema.graphql"
queries_path = "queries.graphql"
```

Run the command:

```bash
$ ariadne-codegen
```

This generates a Python package with a typed client and models.

## Result

### Generated files

The generated package includes a client, base classes, type definitions, and models for each query, mutation, and subscription:

```
graphql_client/
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

The generated client inherits from `AsyncBaseClient` and has async methods for each query, mutation, and subscription you defined.
For example, here is how `create_user`, `list_all_users`, `list_users_by_country`, `get_users_counter`, and `upload_file` are implemented:

```python
# graphql_client/client.py
...
class Client(AsyncBaseClient):
    async def create_user(...): ...
    async def list_all_users(...): ...
    async def list_users_by_country(...): ...
    async def get_users_counter(...): ...
    async def upload_file(...): ...
```

Each method executes the corresponding GraphQL operation and returns a typed Pydantic model.

### Base client

`async_base_client.py` contains the networking logic. It is copied from the file path you specify in `base_client_file_path` and has to define a class named as in `base_client_name`.

### Base model

`base_model.py` defines a Pydantic-based `BaseModel` class. All generated models inherit from this, ensuring validation and serialization work out of the box.

### Input types

Models generated from GraphQL input objects (like `UserCreateInput`) are strongly typed and used as parameters in client methods.

```python
# graphql_client/input_types.py
class UserCreateInput(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    favourite_color: Optional[Color]
    location: Optional["LocationInput"]
```

### Enums

GraphQL enums are converted into Python `Enum` classes. They can be used directly in input types and queries.

```python
# graphql_client/enums.py
class Color(str, Enum):
    BLACK = "BLACK"
    WHITE = "WHITE"
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    YELLOW = "YELLOW"
```

### Query/mutation/subscription types

For each query, mutation, or subscription, a model is generated that mirrors the return type.
For example, here is the type for the `CreateUser` mutation:

```python
# graphql_client/create_user.py
class CreateUser(BaseModel):
    user_create: Optional["CreateUserUserCreate"]
```

Other operations like `ListAllUsers`, `ListUsersByCountry`, and `GetUsersCounter` have their own generated models.

### Fragments file

Fragments defined in your operations are generated as reusable Pydantic models that can be inherited by other result models.

```python
# graphql_client/fragments.py
class BasicUser(BaseModel):
    id: str
    email: str

class UserPersonalData(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
```

### Init file

The `__init__.py` file re-exports all generated classes so they can be imported easily.

```python
# graphql_client/__init__.py
from .client import Client
from .create_user import CreateUser
from .enums import Color
from .fragments import BasicUser, UserPersonalData
...
```

## Using the generated client

Here is how you can use the generated client in your Python application. This shows instantiating the client and calling one of the generated methods.

```python
import asyncio
from graphql_client.client import Client

async def main():
    client = Client(url="http://localhost:8000/graphql")
    users = await client.list_all_users()
    for user in users.users:
        print(user.id, user.first_name, user.last_name, user.email)

asyncio.run(main())
```
