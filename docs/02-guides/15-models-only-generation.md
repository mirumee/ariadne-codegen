---
title: Models only generation
---

# Models only generation


If you only need Pydantic models for a schema (enums, input types, per-query result types and fragments) without a generated `Client`, base client and `exceptions.py`, call `ariadne-codegen` with the `models_only` argument:

```
ariadne-codegen models_only
```

The `models_only` mode reads the same configuration as default client mode. Any schema source described in [Schema sources](./02-schema-sources.md) are supported.

The `queries_path` is optional in this mode; when omitted, only enums, input types and (if any) fragments are generated. When provided, an additional result-type module is emitted for each operation.

Client-specific settings (like `client_name`, `client_file_name`, `base_client_name`, `base_client_file_path`, `async_client`, `opentelemetry_client`, or `enable_custom_operations`) are ignored.
