---
title: Configuration
---

# Configuration

`ariadne-codegen` reads configuration from `[tool.ariadne-codegen]` section in your `pyproject.toml`. You can use other configuration file with `--config` option, eg. `ariadne-codegen --config custom_file.toml`

Minimal configuration for client generation:

```toml
[tool.ariadne-codegen]
schema_path = "schema.graphql"
queries_path = "queries.graphql"
```

## Required settings:

- `queries_path` - path to file/directory with queries (Can be optional if `enable_custom_operations` is used)

One of the following 2 parameters is required, in case of providing both of them `schema_path` is prioritized:

- `schema_path` - path to file/directory with graphql schema
- `remote_schema_url` - url to graphql server, where introspection query can be perfomed

## Optional settings:

- `remote_schema_headers` - extra headers that are passed along with introspection query, eg. `{"Authorization" = "Bearer: token"}`. To include an environment variable in a header value, prefix the variable with `$`, eg. `{"Authorization" = "$AUTH_TOKEN"}`
- `remote_schema_verify_ssl` (defaults to `true`) - a flag that specifies wheter to verify ssl while introspecting remote schema
- `target_package_name` (defaults to `"graphql_client"`) - name of generated package
- `target_package_path` (defaults to cwd) - path where to generate package
- `client_name` (defaults to `"Client"`) - name of generated client class
- `client_file_name` (defaults to `"client"`) - name of file with generated client class
- `base_client_name` (defaults to `"AsyncBaseClient"`) - name of base client class
- `base_client_file_path` (defaults to `.../ariadne_codegen/client_generators/dependencies/async_base_client.py`) - path to file where `base_client_name` is defined
- `enums_module_name` (defaults to `"enums"`) - name of file with generated enums models
- `input_types_module_name` (defaults to `"input_types"`) - name of file with generated input types models
- `fragments_module_name` (defaults to `"fragments"`) - name of file with generated fragments models
- `include_comments` (defaults to `"stable"`) - option which sets content of comments included at the top of every generated file. Valid choices are: `"none"` (no comments), `"timestamp"` (comment with generation timestamp), `"stable"` (comment contains a message that this is a generated file)
- `convert_to_snake_case` (defaults to `true`) - a flag that specifies whether to convert fields and arguments names to snake case
- `include_all_inputs` (defaults to `true`) - a flag specifying whether to include all inputs defined in the schema, or only those used in supplied operations
- `include_all_enums` (defaults to `true`) - a flag specifying whether to include all enums defined in the schema, or only those used in supplied operations
- `async_client` (defaults to `true`) - default generated client is `async`, change this to option `false` to generate synchronous client instead
- `opentelemetry_client` (defaults to `false`) - default base clients don't support any performance tracing. Change this option to `true` to use the base client with Open Telemetry support.
- `files_to_include` (defaults to `[]`) - list of files which will be copied into generated package
- `plugins` (defaults to `[]`) - list of plugins to use during generation
- `enable_custom_operations` (defaults to `false`) - enables building custom operations. Generates additional files that contains all the classes and methods for generation.
