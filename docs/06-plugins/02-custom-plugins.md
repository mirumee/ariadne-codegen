---
title: Custom plugins
---

# How to implement plugin

Plugin is a class extending `ariadne_codegen.plugins.base.Plugin`.

Plugins are instantiated once, at the beginning of `ariadne-codegen` command, with following arguments:

- `schema: GraphQLSchema`: parsed graphql schema
- `config_dict: dict`: parsed `pyproject.toml` file represented as a dictionary

To handle specific events custom plugins need to override [hook methods](#hooks) from default `Plugin`. Default hook methods from `Plugin` don't implement any logic on their own.

## Enabling plugins

Plugins can be enabled in `ariadne-codegen` by assigning list of strings to `plugins` key in config file.
Every element of the list can enable plugins in 2 ways:

1. Providing full import path to class, eg. `my_package.my_plugins.MyPlugin`.

2. Providing only package name, eg. `my_package`. In this case all plugins from selected package will be used. For class to be accessible this way, it needs to be in package's public api. Plugin has to be importable from package, eg. `from my_package import MyPlugin` has to work.

## Plugin execution model

### Sequential pipeline

All plugins run in the order they are listed under `plugins` in `pyproject.toml`. Each plugin receives the **output of the previous plugin** as its input, not the original value. If plugin A and plugin B both implement `generate_client_class`, B sees the `ast.ClassDef` that A already modified.

There is no priority mechanism. Every plugin executes every hook it defines. Order is controlled entirely by the position in the `plugins` list.

### What every plugin instance has

- `self.schema: GraphQLSchema` - the full GraphQL schema, kept up-to-date by `process_schema`
- `self.config_dict: dict` - the parsed `pyproject.toml` as a dict

### What plugins cannot do

- Control or skip other plugins in the chain
- Read the output of sibling plugins
- Prevent the hook chain from continuing
- Write files directly (transform content through code-string hooks; the framework handles writing)

### Two hook levels

**AST-level hooks** (`generate_*_module`, `generate_*_class`, `generate_*_field`, `generate_*_method`, etc.) - fire during code generation, before the AST is serialised to a string. You work with Python `ast` node objects.

**Code-string hooks** (`generate_*_code`, `copy_code`) - fire after AST→string conversion, immediately before each file is written to disk. You work with the final Python source as a plain string. These are the closest equivalent to a file-emission interceptor.

### `process_schema` special case

After each plugin's `process_schema()` returns, `self.schema` is updated on **all** plugin instances - not just the ones that haven't run yet. This guarantees that every subsequent hook in every plugin sees the schema as last modified.

### Post-generation

There is currently no hook that fires after **all** files have been written. The `generate_*_code` / `copy_code` hooks cover per-file interception. If you need a post-generation callback (e.g. to run a formatter over the whole output directory), open an issue.

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
version = 0.21
```

## Hooks

Hooks below are listed in the order they fire during a single `ariadne-codegen` run. Implementing only the hooks you need is fine - the default implementation for every hook returns the input unchanged.

### process_schema

```py
def process_schema(self, schema: GraphQLSchema) -> GraphQLSchema:
```

Called once at startup, immediately after the schema is loaded from path or URL. `assume_valid` is set to `True` during parsing, so `graphql.assert_valid_schema` runs only after this hook returns. This is the earliest point at which plugins can inspect or modify the schema. After each plugin's `process_schema` returns, `self.schema` is updated on **all** plugin instances.

### generate_enum

```py
def generate_enum(self, class_def: ast.ClassDef, enum_type: GraphQLEnumType) -> ast.ClassDef:
```

Called once per enum type in the schema, after the class definition is built but before it is added to the enums module.

### generate_enums_module

```py
def generate_enums_module(self, module: ast.Module) -> ast.Module:
```

Called once, after all enum classes have been generated and collected into the module. Later this module is saved as `{enums_module_name}.py`.

### generate_input_field

```py
def generate_input_field(
    self,
    field_implementation: ast.AnnAssign,
    input_field: GraphQLInputField,
    field_name: str,
) -> ast.AnnAssign:
```

Called once per field in each input type, after the field annotation and default value are generated. Fires before `generate_input_class` for the same class.

### generate_input_class

```py
def generate_input_class(
    self, class_def: ast.ClassDef, input_type: GraphQLInputObjectType
) -> ast.ClassDef:
```

Called once per input type, after all its fields have been generated. Fires after all `generate_input_field` calls for the same class.

### generate_inputs_module

```py
def generate_inputs_module(self, module: ast.Module) -> ast.Module:
```

Called once, after all input classes have been generated and collected. Later this module is saved as `{input_types_module_name}.py`.

### generate_client_import

```py
def generate_client_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
```

Called every time an import statement is registered in any of the generated modules: the client module (`client.py`), and the custom operation modules (`custom_queries.py`, `custom_mutations.py`, `custom_fields.py`). Fires before the import is appended to the module's import list.

### generate_arguments

```py
def generate_arguments(
    self,
    arguments: ast.arguments,
    variable_definitions: Tuple[VariableDefinitionNode, ...],
) -> ast.arguments:
```

Called once per GraphQL operation, after the method's argument list is built from the operation's variable definitions.

### generate_arguments_dict

```py
def generate_arguments_dict(
    self,
    dict_: ast.Dict,
    variable_definitions: Tuple[VariableDefinitionNode, ...],
) -> ast.Dict:
```

Called once per GraphQL operation, immediately after `generate_arguments`, for the `variables` dictionary that is serialised and sent as payload to the GraphQL server.

### generate_client_method

```py
def generate_client_method(
    self,
    method_def: Union[ast.FunctionDef, ast.AsyncFunctionDef],
    operation_definition: OperationDefinitionNode,
) -> Union[ast.FunctionDef, ast.AsyncFunctionDef]:
```

Called once per GraphQL operation, after the full method definition (arguments, body, return type) is assembled. Whether the method is async depends on the `async_client` config option.

### generate_gql_function

```py
def generate_gql_function(self, function_def: ast.FunctionDef) -> ast.FunctionDef:
```

Called once, after all client methods have been added and the `gql()` helper function is generated. Fires before the function is inserted into the client module.

### generate_client_class

```py
def generate_client_class(self, class_def: ast.ClassDef) -> ast.ClassDef:
```

Called once, after all client methods have been added to the client class. At this point `class_def.body` contains every generated method.

### generate_client_module

```py
def generate_client_module(self, module: ast.Module) -> ast.Module:
```

Called once, after the complete client module AST is assembled (imports, `gql` function, client class). Later this module is saved as `{client_file_name}.py`.

### generate_result_field

```py
def generate_result_field(
    self,
    field_implementation: ast.AnnAssign,
    operation_definition: ExecutableDefinitionNode,
    field: FieldNode,
) -> ast.AnnAssign:
```

Called once per field in each result class, after the field type annotation and pydantic metadata (aliases, discriminators, defaults) are applied. Fires before `generate_result_class` for the containing class. Called multiple times per operation - once per field across all result classes in that operation's output file.

### generate_result_class

```py
def generate_result_class(
    self,
    class_def: ast.ClassDef,
    operation_definition: ExecutableDefinitionNode,
    selection_set: SelectionSetNode,
) -> ast.ClassDef:
```

Called once per Pydantic model class in the result file for an operation. There is one class for the top-level result and one for each nested object type selected. Fires after all `generate_result_field` calls for the same class. Called multiple times per operation.

### generate_result_types_module

```py
def generate_result_types_module(
    self, module: ast.Module, operation_definition: ExecutableDefinitionNode
) -> ast.Module:
```

Called once per operation, after all result classes have been assembled into the module. Later this module is saved as `{operation_name}.py`.

### generate_operation_str

```py
def generate_operation_str(
    self, operation_str: str, operation_definition: ExecutableDefinitionNode
) -> str:
```

Called once per operation, for the raw GraphQL query/mutation string that the generated client embeds and sends to the server. Modifying this string changes what the client actually sends - not just the generated Python code.

### generate_fragments_module

```py
def generate_fragments_module(
    self,
    module: ast.Module,
    fragments_definitions: Dict[str, FragmentDefinitionNode],
) -> ast.Module:
```

Called once, after all fragment classes have been generated. Later this module is saved as `{fragments_module_name}.py`. There is no corresponding code-string hook for this file - `fragments.py` is written directly to disk after AST serialisation. Use this hook if you need to modify the fragments output.

### generate_custom_method

```py
def generate_custom_method(self, method_def: ast.FunctionDef) -> ast.FunctionDef:
```

Called once per method in the custom operation builder class. Only fires when `enable_custom_operations = true` is set in config. Fires before `generate_custom_module` for the containing module.

### generate_custom_module

```py
def generate_custom_module(self, module: ast.Module) -> ast.Module:
```

Called once per custom operation module (`custom_queries.py` for queries, `custom_mutations.py` for mutations), after all builder methods have been generated. Only fires when `enable_custom_operations = true`. There is no corresponding code-string hook - these files are written directly after AST serialisation. Note: `custom_fields.py` and `custom_typing_fields.py` have no plugin hook of any kind.

### generate_init_import

```py
def generate_init_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
```

Called once per public symbol re-exported from `__init__.py`, as each import statement is registered. Fires before `generate_init_module`.

### generate_init_module

```py
def generate_init_module(self, module: ast.Module) -> ast.Module:
```

Called once, after all re-export imports have been added to the init module. Later this module is saved as `__init__.py`.

### get_file_comment

```py
def get_file_comment(
    self, comment: str, code: str, source: Optional[str] = None
) -> str:
```

Called once per output file - including copied files (`base_client.py`, `base_model.py`, `exceptions.py`, `files_to_include`) and files that have no code-string hook (`fragments.py`, `custom_queries.py`, `custom_mutations.py`). Fires immediately before the header comment is prepended to the file content. `source` contains the path or URL the file was generated from, or `None` for copied files.

### generate_enums_code

```py
def generate_enums_code(self, generated_code: str) -> str:
```

Called once with the complete `{enums_module_name}.py` source as a string, immediately before the file is written to disk. This is the last point at which the enums file can be modified.

### generate_inputs_code

```py
def generate_inputs_code(self, generated_code: str) -> str:
```

Called once with the complete `{input_types_module_name}.py` source as a string, immediately before the file is written to disk.

### generate_client_code

```py
def generate_client_code(self, generated_code: str) -> str:
```

Called once with the complete `{client_file_name}.py` source as a string, immediately before the file is written to disk.

### generate_result_types_code

```py
def generate_result_types_code(self, generated_code: str) -> str:
```

Called once per operation with the complete `{operation_name}.py` source as a string, immediately before the file is written to disk.

### copy_code

```py
def copy_code(self, copied_code: str) -> str:
```

Called once per copied file, after reading the source but before writing to the output directory. Files: the base client (`*base_client*.py`, selected by config or overridden via `base_client_file_path`), `base_model.py`, `exceptions.py` (built-in clients only), and any `files_to_include`. **This is the only hook that fires for copied files** - AST-level hooks have no effect on them.

### generate_init_code

```py
def generate_init_code(self, generated_code: str) -> str:
```

Called once with the complete `__init__.py` source as a string, immediately before the file is written to disk.

### process_name

```py
def process_name(self, name: str, node: Optional[Node] = None) -> str:
```

Called throughout the entire run, every time a GraphQL field, argument, or operation name is converted to a Python identifier. This hook fires far more frequently than any other - once for each name across all types, operations, and fields. The optional `node` parameter identifies the GraphQL AST node being named.
