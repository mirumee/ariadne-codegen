---
title: Deprecation warnings
---

# Deprecation warnings

`ariadne-codegen` reports deprecated parts of your schema as standard Python `DeprecationWarning`s, so that a client keeps working while the deprecation is surfaced at generation time:

```
ariadne_codegen/client_generators/enums.py:39: DeprecationWarning: Enum value 'OLD_ACTIVE' on enum 'Status' is deprecated: Use NEW_ACTIVE instead.
```

Warnings cover the deprecated parts of the schema your generated package actually uses:

- enum values,
- fields selected by your operations,
- arguments those selections pass,
- fields of the generated input types.

Only what ends up in the generated package is reported. A schema usually defines more enums and inputs than a single client uses, so with `include_all_enums = false` and `include_all_inputs = false` the ones your operations never touch are neither generated nor warned about.

When the schema is introspected from a remote server, deprecated arguments and input fields are only reported with `introspection_input_value_deprecation = true` - without it the server does not send those deprecation reasons at all.

## Turning them off

Set `show_deprecation_warnings` to `false` in your configuration:

```toml
[tool.ariadne-codegen]
show_deprecation_warnings = false
```

## Filtering them

The warnings are ordinary Python warnings, so [`PYTHONWARNINGS`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONWARNINGS) and `python -W` control them. To silence all of them for a single run:

```
PYTHONWARNINGS=ignore::DeprecationWarning ariadne-codegen
```

To turn them into errors instead, so that a deprecation appearing in the schema fails your build:

```
PYTHONWARNINGS=error::DeprecationWarning ariadne-codegen
```

Setting `PYTHONWARNINGS` or `-W` yourself always takes full control of the filters, and takes precedence over `show_deprecation_warnings` - `ariadne-codegen` then adds no filters of its own.

Warnings are written to stderr, separately from the generation progress messages on stdout, so `ariadne-codegen 2>/dev/null` also silences them while keeping the list of generated files.
