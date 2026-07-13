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

Exactly one of the following parameters is required — they are mutually exclusive, so only one schema source may be used at a time (see [Schema sources](../02-guides/02-schema-sources.md)):

- `schema_path` - path to file/directory with graphql schema
- `schema_paths` - list of local paths and/or installed-package sources to build the schema from
- `remote_schema_url` - url to graphql server, where introspection query can be perfomed

## Optional settings:

- `remote_schema_headers` - extra headers that are passed along with introspection query, eg. `{"Authorization" = "Bearer token"}`. To include an environment variable in a header value, prefix the variable with `$`, eg. `{"Authorization" = "$AUTH_TOKEN"}`
- `remote_schema_verify_ssl` (defaults to `true`) - a flag that specifies wheter to verify ssl while introspecting remote schema
- `remote_schema_timeout` (defaults to `5`) - timeout in seconds while introspecting remote schema
- `remote_schema_http_client_path` (defaults to `None`) - dotted import path to a custom HTTP client (a class/callable that returns one, or a ready client object) providing an `httpx`-compatible `post` interface, used only for the remote schema introspection request. If unset, the default `httpx` client is used.
- `target_package_name` (defaults to `"graphql_client"`) - name of generated package
- `target_package_path` (defaults to cwd) - path where to generate package
- `client_name` (defaults to `"Client"`) - name of generated client class
- `client_file_name` (defaults to `"client"`) - name of file with generated client class
- `base_client_name` (defaults to `"AsyncBaseClient"`) - name of base client class
- `base_client_file_path` (defaults to `.../ariadne_codegen/client_generators/dependencies/async_base_client.py`) - path to file where `base_client_name` is defined
- `base_client_module_name` (defaults to the file name of `base_client_file_path`) - name of the module the base client is copied to and imported from in the generated package
- `enums_module_name` (defaults to `"enums"`) - name of file with generated enums models
- `input_types_module_name` (defaults to `"input_types"`) - name of file with generated input types models
- `fragments_module_name` (defaults to `"fragments"`) - name of file with generated fragments models
- `include_comments` (defaults to `"stable"`) - option which sets content of comments included at the top of every generated file. Valid choices are: `"none"` (no comments), `"timestamp"` (comment with generation timestamp), `"stable"` (comment contains a message that this is a generated file)
- `convert_to_snake_case` (defaults to `true`) - a flag that specifies whether to convert fields and arguments names to snake case
- `include_all_inputs` (defaults to `true`) - a flag specifying whether to include all inputs defined in the schema, or only those used in supplied operations
- `include_all_enums` (defaults to `true`) - a flag specifying whether to include all enums defined in the schema, or only those used in supplied operations
- `async_client` (defaults to `true`) - default generated client is `async`, change this to option `false` to generate synchronous client instead
- `opentelemetry_client` (defaults to `false`) - default base clients don't support any performance tracing. Change this option to `true` to use the base client with Open Telemetry support.
- `multipart_uploads` (defaults to `true`) - when set to `false`, a lighter base client variant is generated that omits multipart file upload support.
- `files_to_include` (defaults to `[]`) - list of files which will be copied into generated package
- `plugins` (defaults to `[]`) - list of plugins to use during generation
- `enable_custom_operations` (defaults to `false`) - enables building custom operations. Generates additional files that contains all the classes and methods for generation.
- `include_typename` (defaults to `true`) - a flag that specifies whether to include the `__typename` field in generated models
- `ignore_extra_fields` (defaults to `true`) - when `true`, generated models ignore extra fields returned by the server; set to `false` to add `extra="forbid"` to the base model so unexpected fields raise a validation error
- `default_optional_fields_to_none` (defaults to `false`) - when `true`, optional fields in generated models default to `None` instead of being required keyword arguments
- `skip_validation_rules` (defaults to `["NoUnusedFragments"]`) - list of [graphql-core validation rule](https://github.com/graphql-python/graphql-core) names to skip when validating operations against the schema

### Scalars

Custom scalar mappings are configured in per-scalar subsections rather than a single key:

```toml
[tool.ariadne-codegen.scalars.{graphql scalar name}]
type = "..."
```

See [Custom scalars](../02-guides/06-custom-scalars.md) for the full syntax.

## Introspection query settings:

These options control which fields are included in the GraphQL introspection query when using `remote_schema_url`. See [Schema sources](../02-guides/02-schema-sources.md) for more details.

- `introspection_descriptions` (defaults to `false`) – include descriptions in the introspection result
- `introspection_input_value_deprecation` (defaults to `false`) – include deprecation information for input values
- `introspection_specified_by_url` (defaults to `false`) – include `specifiedByUrl` for custom scalars
- `introspection_schema_description` (defaults to `false`) – include schema description
- `introspection_directive_is_repeatable` (defaults to `false`) – include `isRepeatable` information for directives
- `introspection_input_object_one_of` (defaults to `false`) – include `oneOf` information for input objects

## Related guides

Several settings have dedicated guides that explain them in context:

- [Schema sources](../02-guides/02-schema-sources.md) — `schema_path`, `remote_schema_url`, `remote_schema_*`, and `introspection_*`
- [File uploads](../02-guides/05-file-uploads.md) — `multipart_uploads`
- [Custom scalars](../02-guides/06-custom-scalars.md) — scalar sections and `files_to_include`
- [Async vs sync client](../02-guides/10-async-vs-sync.md) — `async_client`
- [Open Telemetry](../02-guides/09-opentelemetry.md) — `opentelemetry_client`
- [Plugins](../04-plugins/01-intro.md) — `plugins`
- [Custom operation builder](../02-guides/12-custom-operation-builder.md) — `enable_custom_operations`
