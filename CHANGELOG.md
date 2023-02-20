# CHANGELOG

## UNRELEASED

- Changed generated code to pass `mypy --strict`.
- Changed base clients to get full url from user.
- Added support for custom scalars.


## 0.2.1 (2023-02-13)

- Fixed incorrectly raised exception when using custom scalar as query argument type.


## 0.2.0 (2023-02-02)

- Added `remote_schema_url` and `remote_schema_headers` settings to support reading remote schemas.
- Added `headers` argument to `__init__` methods of `BaseClient` and `AsyncBaseClient`.
