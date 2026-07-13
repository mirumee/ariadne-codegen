---
title: Introduction
---

# Plugins

Plugins let you hook into `ariadne-codegen` to inspect or modify the GraphQL schema and the generated code before it is written to disk. A plugin is a Python class extending `ariadne_codegen.plugins.base.Plugin` that overrides one or more [hooks](./03-hooks.md) - each hook fires at a specific point of a generation run and receives the value being produced (a schema, an `ast` node, or a source string), returning it modified or unchanged.

## Why use a plugin

Plugins are the supported extension point when the built-in configuration is not enough. Common use cases:

- **Add file headers** or license banners to every generated module.
- **Inject fields or metadata** into generated Pydantic models (e.g. an `__operation__` marker on result classes).
- **Transform the final source** - rename symbols, rewrite imports, reformat output.
- **Inspect or rewrite the schema** at startup before any code is generated.
- **Read your own configuration** from `pyproject.toml` to drive any of the above.

## Real-world examples

The best worked examples are the [standard plugins](./04-standard-plugins.md) shipped in `ariadne_codegen.contrib` - each is a small, production plugin whose source is worth reading:

- [`ShorterResultsPlugin`](https://github.com/mirumee/ariadne-codegen/blob/main/ariadne_codegen/contrib/shorter_results.py) - rewrites generated client methods to return a single top-level field directly instead of the full result type.
- [`ExtractOperationsPlugin`](https://github.com/mirumee/ariadne-codegen/blob/main/ariadne_codegen/contrib/extract_operations.py) - moves query strings out into a separate module and rewrites the client's imports; also reads its own `[tool.ariadne-codegen.extract-operations]` config.
- [`ClientForwardRefsPlugin`](https://github.com/mirumee/ariadne-codegen/blob/main/ariadne_codegen/contrib/client_forward_refs.py) - moves Pydantic model imports under `TYPE_CHECKING` to speed up importing the client module.
- [`NoReimportsPlugin`](https://github.com/mirumee/ariadne-codegen/blob/main/ariadne_codegen/contrib/no_reimports.py) - empties the generated `__init__.py` to avoid eager initialization of large packages.

## How they work

Plugins are instantiated once, at the start of the `ariadne-codegen` command, and run as a **sequential pipeline** - each plugin receives the output of the previous one. See [Plugin execution model](./02-custom-plugins.md#plugin-execution-model) for the details.

## Next steps

- [Custom plugins](./02-custom-plugins.md) - write and enable your own plugin.
- [Hooks](./03-hooks.md) - the full reference of every hook, in the order it fires.
- [Standard plugins](./04-standard-plugins.md) - ready-to-use plugins shipped with `ariadne-codegen`.
