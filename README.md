[![Ariadne](https://ariadnegraphql.org/img/logo-horizontal-sm.png)](https://ariadnegraphql.org)

[![Build Status](https://github.com/mirumee/ariadne-codegen/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/mirumee/ariadne-codegen/actions)

- - - - -

# Ariadne Code Generator

Python code generator that takes graphql schema, queries, mutations and subscriptions and generates Python package with fully typed and asynchronous GraphQL client.

It's available as `ariadne-codegen` command and reads configuration from the `pyproject.toml` file:

```
$ ariadne-codegen
```

It can also be run as `python -m ariadne_codegen`.


## Features

- Generate pydantic models from schema types, inputs and enums.
- Generate pydantic models for GraphQL results.
- Generate client package with each GraphQL operation available as async method.


## Installation

Ariadne Code Generator can be installed with pip:

```
$ pip install ariadne-codegen
```

To support subscriptions, default base client requires `websockets` package:

```
$ pip install ariadne-codegen[subscriptions]
```


## Configuration

`ariadne-codegen` reads configuration from `[tool.ariadne-codegen]` section in your `pyproject.toml`. You can use other configuration file with `--config` option, eg. `ariadne-codegen --config custom_file.toml`

Minimal configuration for client generation:

```toml
[tool.ariadne-codegen]
schema_path = "schema.graphql"
queries_path = "queries.graphql"
```

Required settings:

- `queries_path` - path to file/directory with queries

One of the following 2 parameters is required, in case of providing both of them `schema_path` is prioritized:

- `schema_path` - path to file/directory with graphql schema
- `remote_schema_url` - url to graphql server, where introspection query can be perfomed

Optional settings:

- `remote_schema_headers` - extra headers that are passed along with introspection query, eg. `{"Authorization" = "Bearer: token"}`. To include an environment variable in a header value, prefix the variable with `$`, eg. `{"Authorization" = "$AUTH_TOKEN"}`
- `remote_schema_verify_ssl` (defaults to `true`) - a flag that specifies wheter to verify ssl while introspecting remote schema
- `target_package_name` (defaults to `"graphql_client"`) - name of generated package
- `target_package_path` (defaults to cwd) - path where to generate package
- `client_name` (defaults to `"Client"`) - name of generated client class
- `client_file_name` (defaults to `"client"`) - name of file with generated client class
- `base_client_name` (defaults to `"AsyncBaseClient"`) - name of base client class
- `base_client_file_path` (defaults to `.../graphql_sdk_gen/generators/async_base_client.py`) - path to file where `base_client_name` is defined
- `enums_module_name` (defaults to `"enums"`) - name of file with generated enums models
- `input_types_module_name` (defaults to `"input_types"`) - name of file with generated input types models
- `fragments_module_name` (defaults to `"fragments"`) - name of file with generated fragments models
- `include_comments` (defaults to `true`) - a flag that specifies whether to include comments in generated files
- `convert_to_snake_case` (defaults to `true`) - a flag that specifies whether to convert fields and arguments names to snake case
- `async_client` (defaults to `true`) - default generated client is `async`, change this to option `false` to generate synchronous client instead
- `files_to_include` (defaults to `[]`) - list of files which will be copied into generated package
- `plugins` (defaults to `[]`) - list of plugins to use during generation


## Plugins

Ariadne Codegen implements a plugin system that enables further customization and fine-tuning of generated Python code. It’s documentation is available separately in the [PLUGINS.md](https://github.com/mirumee/ariadne-codegen/blob/main/PLUGINS.md) file.


### Standard plugins

Ariadne Codegen ships with optional plugins importable from the `ariadne_codegen.contrib` package:

- [`ariadne_codegen.contrib.shorter_results.ShorterResultsPlugin`](ariadne_codegen/contrib/shorter_results.py) - This plugin processes generated client methods for operations where only single top field is requested, so they return this field's value directly instead of operation's result type. For example get_user method generated for query `GetUser() { user(...) { ... }}` will return value of user field directly instead of `GetUserResult`.


## Using generated client

Generated client can be imported from package:
```py
from {target_package_name}.{client_file_name} import {client_name}
```

Example with default settings:
```py
from graphql_client.client import Client
```

### Passing headers to client

Client (with default base client), takes passed headers and attaches them to every sent request.
```py
client = Client("https://example.com/graphql", {"Authorization": "Bearer token"})
```

For more complex scenarios, you can pass your own http client:
```py
client = Client(http_client=CustomComplexHttpClient())
```

`CustomComplexHttpClient` needs to be an instance of `httpx.AsyncClient` for async client, or `httpx.Client` for sync.


### Websockets

To handle subscriptions, default `AsyncBaseClient` uses [websockets](https://github.com/python-websockets/websockets) and implements [graphql-transport-ws](https://github.com/enisdenjo/graphql-ws/blob/master/PROTOCOL.md) subprotocol. Arguments `ws_origin` and `ws_headers` are added as headers to the handshake request and `ws_connection_init_payload` is used as payload of [ConnectionInit](https://github.com/enisdenjo/graphql-ws/blob/master/PROTOCOL.md#connectioninit) message.


## Custom scalars

By default, not built-in scalars are represented as `typing.Any` in generated client.
You can provide information about specific scalar by adding section to `pyproject.toml`:

```toml
[tool.ariadne-codegen.scalars.{graphql scalar name}]
type = "(required) python type name"
serialize = "function used to serialize scalar"
parse = "function used to create scalar instance from serialized form"
```

All occurrences of `{graphql scalar name}` will be represented as `type`. If provided, `serialize` and `parse` will be used for serialization and deserialization.
If `type`/`serialize`/`parse` contains at least one `.` then string will be split by it's last occurrence. First part will be used as module to import from, and second part as type/method name. For example, `type = "custom_scalars.a.ScalarA"` will produce `from custom_scalars.a import ScalarA`.


### Example with scalar mapped to built-in type

In this case scalar is mapped to built-in `str` which doesn't require custom `serialize ` and `parse` methods.

```toml
[tool.ariadne-codegen.scalars.SCALARA]
type = "str"
```


### Example with type supported by pydantic

In this scenario scalar is represented as `datetime`, so it needs to be imported. Pydantic handles serialization and deserialization so custom `parse` and `serialize` is not necessary.

```toml
[tool.ariadne-codegen.scalars.DATETIME]
type = "datetime.datetime"
```


### Example with fully custom type

In this example scalar is represented as class `TypeB`. Pydantic can\`t handle  serialization and deserialization so custom `parse` and `serialize` is necessary. To provide `type`, `parse` and `serialize` implementation we can use `files_to_include` to copy `type_b.py` file.

```toml
[tool.ariadne-codegen]
...
files_to_include = [".../type_b.py"]

[tool.ariadne-codegen.scalars.SCALARB]
type = ".type_b.TypeB"
parse = ".type_b.parse_b"
serialize = ".type_b.serialize_b"
```


## Extending generated types

### Extending models with custom mixins

`mixin` directive allows to extend class generated for query/mutation field with custom logic.
`mixin` takes two required arguments:
- `from` - name of a module to import from
- `import` - name of a parent class

Generated class will use `import` as extra base class, and import will be added to the file.
```py
from {from} import {import}
...
class OperationNameField(BaseModel, {import}):
    ...
```

This directive can be used along with `files_to_include` option to extend functionality of generated classes.


#### Example of usage of `mixin` and `files_to_include`:

Query with `mixin` directive:

```gql
query listUsers {
    users @mixin(from: ".mixins", import: "UsersMixin") {
        id
    }
}
```

Part of `pyproject.toml` with `files_to_include` (`mixins.py` contains `UsersMixin` implementation)
```toml
files_to_include = [".../mixins.py"]
```

Part of generated `list_users.py` file:
```py
...
from .mixins import UsersMixin
...
class ListUsersUsers(BaseModel, UsersMixin):
    ...
```


## Multiple clients

To generate multiple different clients you can store config for each in different file, then provide path to config file by `--config` option, eg.
```
ariadne-codegen --config clientA.toml
ariadne-codegen --config clientB.toml
```


## Generated code dependencies

Generated code requires:

- [pydantic](https://github.com/pydantic/pydantic)
- [httpx](https://github.com/encode/httpx)
- [websockets](https://github.com/python-websockets/websockets) (only for default async base client)

Both `httpx` and `websockets` dependencies can be avoided by providing another base client class with `base_client_file_path` and `base_client_name` options.


## Example

Example with simple schema and few queries and mutations is available [here](https://github.com/mirumee/ariadne-codegen/blob/main/EXAMPLE.md).


## Generating graphql schema's python representation

Instead of generating client, you can generate file with a copy of GraphQL schema as `GraphQLSchema` declaration. To do this call `ariadne-codegen` with `graphqlschema` argument:
```
ariadne-codegen graphqlschema
```

`graphqlschema` mode reads configuration from the same place as [`client`](#configuration) but uses only `schema_path`, `remote_schema_url`, `remote_schema_headers`, `remote_schema_verify_ssl` and `plugins` options with addition to some extra options specific to it:

- `target_file_path` (defaults to `"schema.py"`) - destination path for generated file
- `schema_variable_name` (defaults to `"schema"`) - name for schema variable, must be valid python identifier
- `type_map_variable_name` (defaults to `"type_map"`) - name for type map variable, must be valid python identifier

Generated file contains:

- Necessary imports
- Type map declaration `{type_map_variable_name}: TypeMap = {...}`
- Schema declaration `{schema_variable_name}: GraphQLSchema = GraphQLSchema(...)`


## Contributing

We welcome all contributions to Ariadne! If you've found a bug or issue, feel free to use [GitHub issues](https://github.com/mirumee/ariadne-codegen/issues). If you have any questions or feedback, don't hesitate to catch us on [GitHub discussions](https://github.com/mirumee/ariadne/discussions/).

For guidance and instructions, please see [CONTRIBUTING.md](CONTRIBUTING.md).

Also make sure you follow [@AriadneGraphQL](https://twitter.com/AriadneGraphQL) on Twitter for latest updates, news and random musings!


## **Crafted with ❤️ by [Mirumee Software](http://mirumee.com)** hello@mirumee.com
