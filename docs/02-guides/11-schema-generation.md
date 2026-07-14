---
title: Schema generation
---

# Generating a copy of the GraphQL schema

Instead of generating a client, you can generate a file with a copy of a GraphQL
schema. To do this call `ariadne-codegen` with the `graphqlschema` argument:

```
ariadne-codegen graphqlschema
```

`graphqlschema` mode reads configuration from the same place as the client, but uses
only a subset of the options:

- to retrieve the schema (see [Schema sources](./02-schema-sources.md)):
  - `schema_path`
  - `schema_paths`
  - `remote_schema_url`
  - `remote_schema_headers`
  - `remote_schema_verify_ssl`
  - `remote_schema_timeout`
  - `remote_schema_http_client_path`
  - `introspection_*`
- `plugins` - to load plugins

Before writing the file, the loaded schema is passed through each plugin's
`process_schema` hook and then validated, so this mode can also be used to apply
plugin transformations to a schema or to fail early on an invalid one. See
[Plugins](../04-plugins/01-intro.md) (and the [`process_schema` hook](../04-plugins/03-hooks.md#process_schema))
for details.

In addition to the above, `graphqlschema` mode also accepts additional settings
specific to it:

## `target_file_path`

A string with the destination path for the generated file. Must be either a Python
(`.py`), or GraphQL (`.graphql` or `.gql`) file.

Defaults to `schema.py`.

A generated Python file will contain:

- Necessary imports
- Type map declaration `{type_map_variable_name}: TypeMap = {...}`
- Schema declaration `{schema_variable_name}: GraphQLSchema = GraphQLSchema(...)`

A generated GraphQL file will contain a formatted output of the `print_schema`
function from the `graphql-core` package.

## `schema_variable_name`

A string with a name for the schema variable, must be a valid python identifier.

Defaults to `"schema"`. Used only if the target is a Python file.

## `type_map_variable_name`

A string with a name for the type map variable, must be a valid python identifier.

Defaults to `"type_map"`. Used only if the target is a Python file.

## Example

The output format is chosen from the `target_file_path` extension. To emit a GraphQL
SDL file:

```toml
[tool.ariadne-codegen]
remote_schema_url = "https://example.com/graphql/"
target_file_path = "schema.graphql"
```

These settings live in the same `[tool.ariadne-codegen]` section as the rest of the
configuration - there is no separate subsection for `graphqlschema` mode.

```
ariadne-codegen graphqlschema
```

Point `target_file_path` at a `.py` file instead to emit an importable Python module
with the `schema` / `type_map` variables described above.
