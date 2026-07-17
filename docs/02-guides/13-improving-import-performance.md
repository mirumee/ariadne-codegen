---
title: Improving import performance
---

# Improving import performance for large schemas

For a large schema, most of the time spent importing the generated package goes into defining Pydantic models rather than into your code. Three options address that, and they compose:

```toml
[tool.ariadne-codegen]
defer_model_build = true
use_alias_generator = true
lazy_imports = true
```

The first two make defining a model cheaper. `defer_model_build` sets `defer_build=True` on the generated `BaseModel` and drops the eager `model_rebuild()` calls, so a model's core schema is built the first time it is used instead of at import. `use_alias_generator` sets `alias_generator=to_camel`, which removes the `Field(alias=...)` call from every field whose GraphQL name can be derived from its Python name - each of those calls otherwise constructs two `FieldInfo` objects at import.

`lazy_imports` attacks a different cost: it skips the models you never touch. The generated `__init__.py` normally imports every module in the package, so importing it defines every model whether or not your code uses it. With the setting, `__init__.py` imports a module the first time a name from it is used, through the module-level `__getattr__` [PEP 562](https://peps.python.org/pep-0562/) defines.

A model's core schema inlines the schemas of the types it references, so the cost of building it grows with the schema rather than with the number of models alone. The saving grows the same way:

| settings | 120 object types, 120 input types, 40 operations | 300 input types, 38 fields each |
| --- | --- | --- |
| defaults, no options set | 301 ms | 729 ms |
| `defer_model_build` alone | 165 ms (1.8x) | 340 ms (2.1x) |
| `defer_model_build` + `use_alias_generator` | 124 ms (2.4x) | 233 ms (3.1x) |
| all three | 68 ms (4.4x) | 62 ms (11.8x) |

The numbers are for importing the package *and reaching the client*, which is the smallest thing an application does that has to pay for what the import deferred. Timing `import your_package` on its own would report ~0 ms for the last row and tell you nothing. Absolute times depend on the machine; the ratios are what carry over. The second schema is the one `tests/performance/test_import_performance.py` builds, so you can reproduce that column with `hatch test -- -m performance`.

How much `lazy_imports` is worth depends on the share of the schema you actually use, which is why the two columns differ so widely: the second uses 1 of its 300 input types. Touch every model and it saves nothing - the last row lands back at the one above it, plus a little overhead.

All three options are opt-in, and none changes generated code until you set it: a package generated with the defaults imports in the same time it always did.

`use_alias_generator` needs `pydantic >= 2.8` in the environment that runs the generated package: `to_camel` mangled camelCase names (`firstName` became `firstname`) until [#9561](https://github.com/pydantic/pydantic/pull/9561) fixed it in 2.8, so enabling it raises the generated package's own pydantic requirement to 2.8. `defer_model_build` and `lazy_imports` have no version requirement of their own beyond a supported pydantic 2.x.

`use_alias_generator` does not change what any field is called on the wire. Names that `to_camel` cannot reconstruct keep an explicit `Field(alias=...)`: `__typename`, keyword-escaped names such as `list_`, acronyms such as `productID`, and schemas whose fields are already snake_case (`some_field` would otherwise become `someField`). The same holds with `convert_to_snake_case = false`, where field names already match the schema and every renamed field keeps its alias - which also means there is nothing to gain there, so leave `use_alias_generator` off unless you convert to snake_case.

Some caveats. `defer_model_build` moves the build cost to first use rather than removing it, so a short-lived process that touches every model pays it anyway - and the same goes for `lazy_imports`. Because `alias_generator` is set on the shared `BaseModel`, it also applies to fields you add through [custom mixins](./07-extending-types.md#extending-models-with-custom-mixins) - name those in snake_case and they will be aliased to camelCase.

`lazy_imports` turns the `ClientForwardRefsPlugin` on for you, and it needs to: the lazy `__init__` stops the package importing every module, and the plugin stops `client.py` importing the input types it only names in annotations. With either one alone the other still pulls the models in, and the import costs what it always did. The plugin is appended after any plugin you configured yourself, because it rewrites the client module they produce; listing it yourself as well changes nothing.

Deferring an import defers what it would have raised. A module that fails to import - a broken [custom mixin](./07-extending-types.md#extending-models-with-custom-mixins), say - surfaces when the name is first used rather than at `import your_package`. `__all__` is unchanged, so `from your_package import *` and any explicit import of a name still behave as before.
