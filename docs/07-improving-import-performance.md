---
title: Improving import performance
---

# Improving import performance for large schemas

For a large schema, most of the time spent importing the generated package goes into defining Pydantic models rather than into your code. Two options address that, and they compose:

```toml
[tool.ariadne-codegen]
defer_model_build = true
use_alias_generator = true
```

`defer_model_build` sets `defer_build=True` on the generated `BaseModel` and drops the eager `model_rebuild()` calls, so a model's core schema is built the first time it is used instead of at import. `use_alias_generator` sets `alias_generator=to_camel`, which removes the `Field(alias=...)` call from every field whose GraphQL name can be derived from its Python name - each of those calls otherwise constructs two `FieldInfo` objects at import.

A model's core schema inlines the schemas of the types it references, so the cost of building it grows with the schema rather than with the number of models alone. The saving grows the same way:

| settings | 120 object types, 120 input types, 40 operations | 300 input types, 38 fields each |
| --- | --- | --- |
| defaults, neither option set | 216 ms | 552 ms |
| `defer_model_build` alone | 134 ms (1.6x) | 293 ms (1.9x) |
| `defer_model_build` + `use_alias_generator` | 100 ms (2.2x) | 194 ms (2.8x) |

Absolute times depend on the machine; the ratios are what carry over. The second schema is the one `tests/performance/test_import_performance.py` builds, so you can reproduce that column with `hatch test -- -m performance`.

Both options are opt-in, and neither changes generated code until you set it: a package generated with the defaults imports in the same time it always did.

`use_alias_generator` needs `pydantic >= 2.8` in the environment that runs the generated package: `to_camel` mangled camelCase names (`firstName` became `firstname`) until [#9561](https://github.com/pydantic/pydantic/pull/9561) fixed it in 2.8, so enabling it raises the generated package's own pydantic requirement to 2.8. `defer_model_build` works with any supported pydantic 2.x.

`use_alias_generator` does not change what any field is called on the wire. Names that `to_camel` cannot reconstruct keep an explicit `Field(alias=...)`: `__typename`, keyword-escaped names such as `list_`, acronyms such as `productID`, and schemas whose fields are already snake_case (`some_field` would otherwise become `someField`). The same holds with `convert_to_snake_case = false`, where field names already match the schema and every renamed field keeps its alias - which also means there is nothing to gain there, so leave `use_alias_generator` off unless you convert to snake_case.

Two caveats. `defer_model_build` moves the build cost to first use rather than removing it, so a short-lived process that touches every model pays it anyway. And because `alias_generator` is set on the shared `BaseModel`, it also applies to fields you add through [custom mixins](https://github.com/mirumee/ariadne-codegen/blob/main/README.md#extending-models-with-custom-mixins) - name those in snake_case and they will be aliased to camelCase.
