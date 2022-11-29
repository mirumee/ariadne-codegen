# graphql-sdk-gen

`graphql-sdk-gen` is a code generator that takes graphql schema, queries and mutations to generate fully typed and asynchronous python client.


## Features

- Generate pydantic models from schema types, inputs and enums.
- Generate pydnatic models for GraphQL results.
- Generate client package with each GraphQL operation available as async method.


## Installation

graphql-sdk-gen can be installed by:

using [poetry](https://python-poetry.org/)
```
poetry add git+https://github.com/mirumee/graphql-sdk-gen.git@main
```

or using pip
```
pip install git+https://github.com/mirumee/graphql-sdk-gen.git@main
```


## Configuration

graphql-sdk-gen reads configuration from `pyproject.toml` from `[graphql-sdk-gen]` section.

Required parameters:

- `schema_path` - path to file/directory with graphql schema
- `queries_path` - path to file/directory with queries

Optional parameters:

- `target_package_name` (defaults to `"graphql_client"`) - name of generated package
- `target_package_path` (defaults to cwd) - path where to generate package
- `client_name` (defaults to `"Client"`) - name of generated client class
- `client_file_name` (defaults to `"client"`) - name of file with generated client class
- `base_client_name` (defaults to `"BaseClient"`) - name of base client class
- `base_client_file_path` (defaults to `.../graphql_sdk_gen/generators/base_client.py`) - path to file where `base_client_name` is defined
- `schema_types_module_name` (defaults to `"schema_types"`) - name of file with generated schema types models
- `enums_module_name` (defaults to `"enums"`) - name of file with generated enums models
- `input_types_module_name` (defaults to `"input_types"`) - name of file with generated input types models
- `include_comments` (defaults to `True`) - a flag that specifies whether to include comments in generated files
- `convert_to_snake_case` (defaults to `True`) - a flag that specifies whether to convert fields and arguments names to snake case


## Usage

Command from below reads [configuration](#configuration) and generates files into `target_package_path/target_package_name` directory:

```
graphql-sdk-gen
```


## Generated code dependencies

Generated code requires:

- pydantic
- httpx (can be avoided by providing another base client class with `base_client_file_path` and `base_client_name` parameters)


## Example

Example with simple schema and few queries and mutations is available [here](./EXAMPLE.md).

<br>

## **Crafted with ❤️ by [Mirumee Software](http://mirumee.com)** hello@mirumee.com
