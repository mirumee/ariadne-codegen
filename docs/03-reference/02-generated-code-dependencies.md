---
title: Generated code dependencies
---

# Generated code dependencies

Generated code requires:

- [pydantic](https://github.com/pydantic/pydantic)
- [httpx](https://github.com/encode/httpx)
- [websockets](https://github.com/python-websockets/websockets) (only for the default async base client)
- [graphql-core](https://github.com/graphql-python/graphql-core) (only when `enable_custom_operations` is used)

## When each dependency is required

- **pydantic** is always required — all generated models (inputs, enums, results,
  fragments) inherit from a pydantic `BaseModel`.
- **httpx** is required by the default base clients (`AsyncBaseClient` and
  `BaseClient`), which use it to perform HTTP requests.
- **websockets** is required only by the default async base client
  (`AsyncBaseClient`), and only when handling subscriptions over WebSockets. See
  [Subscriptions](../02-guides/04-subscriptions.md).
- **graphql-core** is required only when the custom operation builder is enabled
  (`enable_custom_operations = true`); the generated `client.py` and `base_operation.py`
  then import GraphQL AST nodes from it. Regular generated clients do not import it.
  See [Custom operation builder](../02-guides/12-custom-operation-builder.md).

## Avoiding httpx and websockets

Both the `httpx` and `websockets` dependencies can be avoided by providing another
base client class with the `base_client_file_path` and `base_client_name` options.
When you supply your own base client, `ariadne-codegen` copies it into the generated
package instead of the default one, so the generated code only depends on whatever
your base client imports.

```toml
[tool.ariadne-codegen]
base_client_file_path = "path/to/custom_base_client.py"
base_client_name = "CustomBaseClient"
```
