---
title: Custom plugins
---

# Custom plugins

Plugin is a class extending `ariadne_codegen.plugins.base.Plugin`.

Plugins are instantiated once, at the beginning of `ariadne-codegen` command, with following arguments:

- `schema: GraphQLSchema`: parsed graphql schema
- `config_dict: dict`: parsed `pyproject.toml` file represented as a dictionary

To handle specific events custom plugins need to override [hook methods](./03-hooks.md) from default `Plugin`. Default hook methods from `Plugin` don't implement any logic on their own.

## Enabling plugins

Plugins can be enabled in `ariadne-codegen` by assigning list of strings to `plugins` key in config file.
Every element of the list can enable plugins in 2 ways:

1. Providing full import path to class, eg. `my_package.my_plugins.MyPlugin`.

2. Providing only package name, eg. `my_package`. In this case all plugins from selected package will be used. For class to be accessible this way, it needs to be in package's public api. Plugin has to be importable from package, eg. `from my_package import MyPlugin` has to work.

## Plugin execution model

### Sequential pipeline

All plugins run in the order they are listed under `plugins` in `pyproject.toml`. Each plugin receives the **output of the previous plugin** as its input, not the original value.

There is no priority mechanism. Every plugin executes every hook it defines. Order is controlled entirely by the position in the `plugins` list.

### Two hook levels

**AST-level hooks** (`generate_*_module`, `generate_*_class`, `generate_*_field`, `generate_*_method`, etc.) - fire during code generation, before the AST is serialised to a string. You work with Python `ast` node objects.

**Code-string hooks** (`generate_*_code`, `copy_code`) - fire after AST→string conversion, immediately before each file is written to disk. You work with the final Python source as a plain string. These are the closest equivalent to a file-emission interceptor.

### `process_schema` special case

After each plugin's `process_schema()` returns, `self.schema` is updated on **all** plugin instances - not just the ones that haven't run yet. This guarantees that every subsequent hook in every plugin sees the schema as last modified.

### Post-generation

There is currently no hook that fires after **all** files have been written. The `generate_*_code` / `copy_code` hooks cover per-file interception. If you need a post-generation callback (e.g. to run a formatter over the whole output directory), open an issue.

### Custom operations and fields coverage

The files generated with `enable_custom_operations = true` are reached by only a few hooks. None of them have a code-string hook, and the custom-fields files have no dedicated AST hook.

| File | AST hook | `generate_client_import` | `get_file_comment` |
|------|----------|:---:|:---:|
| `custom_queries.py` / `custom_mutations.py` | `generate_custom_method`, `generate_custom_module` | ✅ | ✅ |
| `custom_fields.py` | none | ✅ | ✅ |
| `custom_typing_fields.py` | none | none | ✅ |

## Examples

### Pipeline - two plugins on the same hook

`PluginA` and `PluginB` both implement `generate_client_class`. When registered as `plugins = ["my_pkg.PluginA", "my_pkg.PluginB"]`, `PluginB` receives the `class_def` already modified by `PluginA`.

```py
import ast
from ariadne_codegen.plugins.base import Plugin


class PluginA(Plugin):
    def generate_client_class(self, class_def: ast.ClassDef) -> ast.ClassDef:
        docstring = ast.Expr(value=ast.Constant(value="Auto-generated client."))
        class_def.body.insert(0, docstring)
        return class_def


class PluginB(Plugin):
    def generate_client_class(self, class_def: ast.ClassDef) -> ast.ClassDef:
        # class_def.body[0] is already the docstring inserted by PluginA
        class_def.name = "Generated" + class_def.name
        return class_def
```

Result in `client.py`:

```py
class GeneratedClient(AsyncBaseClient):
    """Auto-generated client."""
    ...
```

### AST hook - adding a field to every result class

`generate_result_class` fires once per Pydantic model class inside a result file (e.g. `get_user.py`). There can be multiple classes per operation - one for the top-level result and one for each nested type. This plugin adds `__operation__: str = "GetUser"` as the first field of every result class.

```py
import ast
from ariadne_codegen.plugins.base import Plugin


class ASTPlugin(Plugin):
    def generate_result_class(
        self, class_def, operation_definition, selection_set
    ) -> ast.ClassDef:
        op_name = (
            operation_definition.name.value if operation_definition.name else "unknown"
        )
        attr = ast.AnnAssign(
            target=ast.Name(id="__operation__"),
            annotation=ast.Name(id="str"),
            value=ast.Constant(value=op_name),
            simple=1,
            lineno=1,
            col_offset=0,
        )
        class_def.body.insert(0, attr)
        return class_def
```

### Code-string hook - adding a header to generated files

`generate_client_code` and `generate_enums_code` receive the final Python source as a plain string, immediately before the file is written to disk. This is the right place for text-based transformations that are simpler to do on a string than on an AST.

```py
from ariadne_codegen.plugins.base import Plugin


class HeaderPlugin(Plugin):
    def generate_client_code(self, generated_code: str) -> str:
        header = "\n".join([
            "# ──────────────────────────────────────────",
            "# Auto-generated - do not edit manually",
            "# Generated by ariadne-codegen",
            "# ──────────────────────────────────────────",
            "",
        ])
        return header + generated_code

    def generate_enums_code(self, generated_code: str) -> str:
        return self.generate_client_code(generated_code)
```

### `process_schema` - inspecting the schema at startup

`process_schema` runs once, before any file is generated. `self.schema` on all plugin instances is updated after each plugin's `process_schema` returns, so every subsequent hook call sees the latest schema.

```py
from graphql import GraphQLSchema
from ariadne_codegen.plugins.base import Plugin


class SchemaPlugin(Plugin):
    def process_schema(self, schema: GraphQLSchema) -> GraphQLSchema:
        query_type = schema.query_type
        if query_type and "_version" not in query_type.fields:
            print("[SchemaPlugin] Query type is missing _version field")
        # Return the schema unmodified, or return a new GraphQLSchema to replace it.
        return schema
```

### Reading config - VersionPlugin

Adds `__version__ = "..."` to the generated `__init__.py` by reading a value from `pyproject.toml`.

```py
import ast

from ariadne_codegen.plugins.base import Plugin


class VersionPlugin(Plugin):
    def generate_init_module(self, module: ast.Module) -> ast.Module:
        version = (
            self.config_dict.get("tool", {})
            .get("version_plugin", {})
            .get("version", "0.1")
        )
        assign = ast.Assign(
            targets=[ast.Name(id="__version__")],
            value=ast.Constant(value=version),
            lineno=len(module.body) + 1,
        )
        module.body.append(assign)
        return module
```

```toml
[tool.version_plugin]
version = "0.21"
```
