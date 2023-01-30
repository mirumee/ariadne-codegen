[![Ariadne](https://ariadnegraphql.org/img/logo-horizontal-sm.png)](https://ariadnegraphql.org)

[![Build Status](https://github.com/mirumee/ariadne-codegen/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/mirumee/ariadne-codegen/actions)

- - - - -

# Ariadne Code Generator

Python code generator that takes graphql schema, queries and mutations and generates Python package with fully typed and asynchronous GraphQL client.

It's available as `ariadne-codegen` command and reads configuration from the `pyproject.toml` file:

```
$ ariadne-codegen
```


## Features

- Generate pydantic models from schema types, inputs and enums.
- Generate pydnatic models for GraphQL results.
- Generate client package with each GraphQL operation available as async method.


## Installation

Ariadne Code Generator can be installed with pip:

```
$ pip install ariadne-codegen
```


## Configuration

`ariadne-codegen` reads configuration from `[ariadne-codegen]` section in your `pyproject.toml`'.

Required settings:

- `schema_path` - path to file/directory with graphql schema
- `queries_path` - path to file/directory with queries

Optional settings:

- `target_package_name` (defaults to `"graphql_client"`) - name of generated package
- `target_package_path` (defaults to cwd) - path where to generate package
- `client_name` (defaults to `"Client"`) - name of generated client class
- `client_file_name` (defaults to `"client"`) - name of file with generated client class
- `base_client_name` (defaults to `"AsyncBaseClient"`) - name of base client class
- `base_client_file_path` (defaults to `.../graphql_sdk_gen/generators/async_base_client.py`) - path to file where `base_client_name` is defined
- `enums_module_name` (defaults to `"enums"`) - name of file with generated enums models
- `input_types_module_name` (defaults to `"input_types"`) - name of file with generated input types models
- `include_comments` (defaults to `True`) - a flag that specifies whether to include comments in generated files
- `convert_to_snake_case` (defaults to `True`) - a flag that specifies whether to convert fields and arguments names to snake case
- `async_client` (defaults to `True`) - a flag that specifies whether to generate client with async methods
- `files_to_include` (defaults to `[]`) - list of files which will be copied into generated package


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

This directive can be used along with `files_to_include` option to extend funcionallity of generated classes.


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


## Generated code dependencies

Generated code requires:

- pydantic
- httpx (can be avoided by providing another base client class with `base_client_file_path` and `base_client_name` parameters)


## Example

Example with simple schema and few queries and mutations is available [here](./EXAMPLE.md).


## Contributing

We welcome all contributions to Ariadne! If you've found a bug or issue, feel free to use [GitHub issues](https://github.com/mirumee/ariadne-codegen/issues). If you have any questions or feedback, don't hesitate to catch us on [GitHub discussions](https://github.com/mirumee/ariadne/discussions/).

Also make sure you follow [@AriadneGraphQL](https://twitter.com/AriadneGraphQL) on Twitter for latest updates, news and random musings!


## **Crafted with ❤️ by [Mirumee Software](http://mirumee.com)** hello@mirumee.com
