---
title: Schema sources
---

# Schema sources

`ariadne-codegen` needs a GraphQL schema to generate a client. You can provide it
from a local file/directory, from installed Python packages, or by introspecting a
remote GraphQL server.

Exactly one of the following settings is required — `schema_path`, `schema_paths`
and `remote_schema_url` are **mutually exclusive**, so only one schema source may be
used at a time:

- `schema_path` - path to file/directory with GraphQL schema
- `schema_paths` - list of local paths and/or installed-package sources to build the schema from
- `remote_schema_url` - url to GraphQL server, where introspection query can be performed

## Local schema file

Point `schema_path` at a `.graphql` file or a directory containing schema files:

```toml
[tool.ariadne-codegen]
schema_path = "schema.graphql"
queries_path = "queries.graphql"
```

## Loading schema from installed packages

`schema_paths` lets you pull type definitions from installed Python packages
alongside your local schema files, so codegen can resolve types that live in a
shared library without copying them manually.

Each entry in `schema_paths` is first tried as a local filesystem path, and if it
is neither an existing file nor directory it is treated as a dotted Python import
path. An entry must be one of the following:

- a path to a directory — all `.graphql`, `.graphqls` and `.gql` files from it are included (searched recursively), eg. `./my_schemas/`
- a path to a specific file to be used, eg. `./shared/types.graphql`
- an absolute import path to a callable that returns a `list[str]` of file paths, eg. `some_package.get_schema_files`
- an absolute import path to a variable holding the path to a single schema file, eg. `some_package.SCHEMA_FILE`
- an absolute import path to a variable holding the path to a directory — all `.graphql`, `.graphqls` and `.gql` files from it are included, eg. `some_package.SCHEMA_DIR`

```toml
[tool.ariadne-codegen]
schema_paths = [
  "some_gql_commontypes.get_schema_files",   # callable → returns list of paths
  "other_pkg.SCHEMA_DIR",                     # variable → directory
  "./my_other_packages/",                     # local directory
  "./foo/bar.graphql",                        # local file
]
queries_path = "queries.graphql"
```

## Remote schema introspection

Set `remote_schema_url` to a GraphQL endpoint and `ariadne-codegen` will run an
introspection query to retrieve the schema:

```toml
[tool.ariadne-codegen]
remote_schema_url = "https://example.com/graphql/"
queries_path = "queries.graphql"
```

The following options control how the introspection request is performed:

- `remote_schema_headers` - extra headers that are passed along with introspection query, eg. `{"Authorization" = "Bearer token"}`. To include an environment variable in a header value, prefix the variable with `$`, eg. `{"Authorization" = "$AUTH_TOKEN"}`
- `remote_schema_verify_ssl` (defaults to `true`) - a flag that specifies whether to verify ssl while introspecting remote schema
- `remote_schema_timeout` (defaults to `5`) - timeout in seconds while introspecting remote schema

## Introspection query options

These options only apply when the schema is fetched via `remote_schema_url`. They
map directly to the arguments of `graphql-core`'s
[`get_introspection_query()`](https://graphql-core-3.readthedocs.io/en/latest/modules/utilities.html#graphql.utilities.get_introspection_query)
(the config key `introspection_<name>` becomes the `<name>` argument), and they
control which optional fields the generated introspection query asks the server
for. They have no effect when using a local `schema_path` / `schema_paths`, because
a local SDL already contains everything.

```toml
[tool.ariadne-codegen]
remote_schema_url = "https://example.com/graphql/"
queries_path = "queries.graphql"
introspection_descriptions = true
```

- `introspection_descriptions` (defaults to `false`) – include descriptions in the introspection result
- `introspection_input_value_deprecation` (defaults to `false`) – include deprecation information for input values
- `introspection_specified_by_url` (defaults to `false`) – include `specifiedByUrl` for custom scalars
- `introspection_schema_description` (defaults to `false`) – include schema description
- `introspection_directive_is_repeatable` (defaults to `false`) – include `isRepeatable` information for directives
- `introspection_input_object_one_of` (defaults to `false`) – include `oneOf` information for input objects
