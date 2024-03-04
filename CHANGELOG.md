# CHANGELOG

## 0.13.0 (2024-03-4)

- Fixed `str_to_snake_case` utility to capture fully capitalized words followed by an underscore.
- Re-added `model_rebuild` calls for models with forward references.
- Fixed potential name conflicts between field args and generated client's method code.


## 0.12.0 (2024-02-05)

- Fixed `graphql-transport-ws` protocol implementation not waiting for the `connection_ack` message on new connection.
- Fixed `get_client_settings` mutating `config_dict` instance.
- Added support to `graphqlschema` for saving schema as a GraphQL file.
- Restored `model_rebuild` calls for top level fragment models.


## 0.11.0 (2023-12-05)

- Removed `model_rebuild` calls for generated input, fragment and result models. 
- Added `NoReimportsPlugin` that makes the `__init__.py` of generated client package empty.
- Added `include_all_inputs` config flag to generate only inputs used in supplied operations.
- Added `include_all_enums` config flag to generate only enums used in supplied operations.
- Added `operationName` to payload sent by generated client's methods.
- Fixed base clients to pass `mypy --strict` without installed optional dependencies.
- Renamed `GraphQlClientInvalidResponseError` to `GraphQLClientInvalidResponseError` (breaking change).
- Changed base clients to raise `GraphQLClientGraphQLMultiError` for payloads with `errors` key but no `data` (breaking change).


## 0.10.0 (2023-11-15)

- Fixed generating results for nullable fields with nullable directives.
- Changed `include_comments` option to accept enum value, changed default to `"stable"`, deprecated boolean support. Added `get_file_comment` plugin hook.
- Changed `str_to_snake_case` utility to correctly handle capitalized words.
- Digits in Python names are now preceded by an underscore (breaking change).
- Fixed parsing of unions and interfaces to always add `__typename` to generated result models.
- Added escaping of enum values which are Python keywords by appending `_` to them.
- Fixed `enums_module_name` option not being passed to generators.
- Added additional base clients supporting the Open Telemetry tracing. Added `opentelemetry_client` config option.
- Changed generated client's methods to pass `**kwargs` to base client's `execute` and `execute_ws` methods (breaking change for custom base clients).
- Added `operation_definition` argument to `generate_client_method` plugin hook.
- Added `ExtractOperationsPlugin` that extracts operation strings from client methods to separate module.
- Added Python 3.12 to tested versions.


## 0.9.0 (2023-09-11)

- Fixed generating operation string for nested inline fragments.
- Removed scalars module. Changed generated models and client to use annotated types for custom scalars. Removed `scalars_module_name` option. Removed `generate_scalars_module`, `generate_scalars_cod`, `generate_scalar_annotation` and `generate_scalar_imports` plugin hooks.
- Removed pydantic warnings for fields with `model_` prefix.
- Fixed generating result types with nullable directives.


## 0.8.0 (2023-08-22)

- Added support for `Upload` scalar. Added support for file uploads to `AsyncBaseClient` and `BaseClient`.
- Added validation of defined operations against the schema.
- Removed `mixin` directive from fragment string included in operation string sent to server.
- Added support for `mixin` directive on fragments definitions.
- Added support for fragments defined on subtype of field's type.
- Added default representation for a field name consisting only of underscores.
- Changed generated client and models to use pydantic v2.
- Changed custom scalars implementation to utilize pydantic's `BeforeValidator` and `PlainSerializer`. Added `scalars_module_name` option. Replaced `generate_scalars_parse_dict` and `generate_scalars_serialize_dict` with `generate_scalar_annotation` and `generate_scalar_imports` plugin hooks.
- Unified annotations in generated client to be compatible with python < 3.9.
- Fixed generating default values of input types from remote schemas.
- Changed generating of input and result field names to add `_` to names reserved by pydantic.


## 0.7.1 (2023-06-06)

- Fixed `AsyncBaseClient` and `BaseClient` to send `Content-Type` header with requests.


## 0.7.0 (2023-06-01)

- Added support for subscriptions as async generators.
- Changed how fragments are handled to generate separate module with fragments as mixins.
- Fixed `ResultTypesGenerator` to trigger `generate_result_class` for each result model.
- Changed processing of models fields to trim leading underscores.
- Added `ShorterResultsPlugin` to standard plugins.
- Fixed handling of inline fragments inside other fragments.
- Changed generated unions to use pydantic's discriminated unions feature.
- Replaced HTTPX's `json=` serializer for query payloads with pydantic's `pydantic_encoder`.
- Removed `mixin` directive from operation string sent to server.
- Fixed `ShorterResultsPlugin` that generated faulty code for discriminated unions.
- Changed generator to ignore unused fragments which should be unpacked in queries.
- Changed type hints for parse and serialize methods of scalars to `typing.Any`.
- Added `process_schema` plugin hook.


## 0.6.0 (2023-04-18)

- Changed logic how custom scalar imports are generated. Deprecated `import_` key.
- Added escaping of GraphQL names which are Python keywords by appending `_` to them.
- Fixed parsing of list variables.
- Changed base clients to remove unset arguments and input fields from variables payload.
- Added `process_name` plugin hook.


## 0.5.0 (2023-04-05)

- Added generation of GraphQL schema's Python representation.
- Fixed annotations for lists.
- Fixed support of custom operation types names.
- Unlocked versions of black, isort, autoflake and dev dependencies
- Added `remote_schema_verify_ssl` option.
- Changed how default values for inputs are generated to handle potential cycles.
- Fixed `BaseModel` incorrectly calling `parse` and `serialize` methods on entire list instead of its items for `List[Scalar]`.


## 0.4.0 (2023-03-20)

- Fixed generating models from interfaces with inline fragments.
- Added default `None` values for generated methods optional arguments.
- Added basic plugin system.
- Added `InitFileGenerator`, `EnumsGenerator`, `ClientGenerator` and `ArgumentsGenerator` plugin hooks.
- Added `InputTypesGenerator` and `ResultTypesGenerator` plugin hooks.
- Added `ScalarsDefinitionsGenerator` and `PackageGenerator` plugin hooks.
- Added support for `[tool.ariadne-codegen]` section key. Deprecated `[ariadne-codegen]`.
- Added support for environment variables to remote schema headers values.
- Added `--config` argument to `ariadne-codegen` script, to support reading configuration from custom path.


## 0.3.0 (2023-02-21)

- Changed generated code to pass `mypy --strict`.
- Changed base clients to get full url from user.
- Added support for custom scalars.


## 0.2.1 (2023-02-13)

- Fixed incorrectly raised exception when using custom scalar as query argument type.


## 0.2.0 (2023-02-02)

- Added `remote_schema_url` and `remote_schema_headers` settings to support reading remote schemas.
- Added `headers` argument to `__init__` methods of `BaseClient` and `AsyncBaseClient`.
