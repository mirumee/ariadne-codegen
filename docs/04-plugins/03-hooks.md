---
title: Hooks
---

# Hooks

Hooks are the methods a custom plugin overrides to take part in code generation. They are defined on the base `Plugin` class in [`ariadne_codegen/plugins/base.py`](https://github.com/mirumee/ariadne-codegen/blob/main/ariadne_codegen/plugins/base.py) (importable as `ariadne_codegen.plugins.base.Plugin`).

Every hook has a default implementation that returns its input unchanged, so a plugin only needs to override the hooks it cares about. See [Custom plugins](./02-custom-plugins.md) for how to write and enable a plugin.

Hooks below are listed in the order they fire during a single `ariadne-codegen` run.


### process_schema

```py
def process_schema(self, schema: GraphQLSchema) -> GraphQLSchema:
```

Called once at startup, immediately after the schema is loaded from path or URL and before it is validated. The schema is built with `assume_valid=True` (in [`ariadne_codegen/schema.py`](https://github.com/mirumee/ariadne-codegen/blob/main/ariadne_codegen/schema.py)), which defers validation: `ariadne-codegen` only calls `graphql.assert_valid_schema` *after* this hook returns (see [`main.py`](https://github.com/mirumee/ariadne-codegen/blob/main/ariadne_codegen/main.py)). That makes `process_schema` the one place where a plugin can repair a schema that would otherwise fail validation. It is also the earliest point at which plugins can inspect or modify the schema. After each plugin's `process_schema` returns, `self.schema` is updated on **all** plugin instances.

### generate_client_import

```py
def generate_client_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
```

Called every time an import statement is registered in any of the generated modules: the client module (`client.py`), and the custom operation modules (`custom_queries.py`, `custom_mutations.py`, `custom_fields.py`). Fires before the import is appended to the module's import list.

### process_name

```py
def process_name(self, name: str, node: Optional[Node] = None) -> str:
```

Called throughout the entire run, every time a GraphQL field, argument, or operation name is converted to a Python identifier. This hook fires far more frequently than any other - once for each name across all types, operations, and fields. The optional `node` parameter identifies the GraphQL AST node being named.

### generate_enum

```py
def generate_enum(self, class_def: ast.ClassDef, enum_type: GraphQLEnumType) -> ast.ClassDef:
```

Called once per enum type in the schema, after the class definition is built but before it is added to the enums module.

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

### generate_init_import

```py
def generate_init_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
```

Called once per public symbol re-exported from `__init__.py`, as each import statement is registered. Fires before `generate_init_module`.

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

### generate_inputs_module

```py
def generate_inputs_module(self, module: ast.Module) -> ast.Module:
```

Called once, after all input classes have been generated and collected. Later this module is saved as `{input_types_module_name}.py`.

### get_file_comment

```py
def get_file_comment(
    self, comment: str, code: str, source: Optional[str] = None
) -> str:
```

Called once per output file - including copied files (`base_client.py`, `base_model.py`, `exceptions.py`, `files_to_include`) and files that have no code-string hook (`fragments.py`, `custom_queries.py`, `custom_mutations.py`). Fires immediately before the header comment is prepended to the file content. `source` contains the path or URL the file was generated from, or `None` for copied files.

### generate_inputs_code

```py
def generate_inputs_code(self, generated_code: str) -> str:
```

Called once with the complete `{input_types_module_name}.py` source as a string, immediately before the file is written to disk.

### generate_result_types_code

```py
def generate_result_types_code(self, generated_code: str) -> str:
```

Called once per operation with the complete `{operation_name}.py` source as a string, immediately before the file is written to disk.

### generate_fragments_module

```py
def generate_fragments_module(
    self,
    module: ast.Module,
    fragments_definitions: Dict[str, FragmentDefinitionNode],
) -> ast.Module:
```

Called once, after all fragment classes have been generated. Later this module is saved as `{fragments_module_name}.py`. There is no corresponding code-string hook for this file - `fragments.py` is written directly to disk after AST serialisation. Use this hook if you need to modify the fragments output.

### copy_code

```py
def copy_code(self, copied_code: str) -> str:
```

Called once per copied file, after reading the source but before writing to the output directory. Files: the base client (`*base_client*.py`, selected by config or overridden via `base_client_file_path`), `base_model.py`, `exceptions.py` (built-in clients only), and any `files_to_include`. **This is the only hook that fires for copied files** - AST-level hooks have no effect on them.

### generate_custom_method

```py
def generate_custom_method(self, method_def: ast.FunctionDef) -> ast.FunctionDef:
```

Called once per method in the custom operation builder class. Only fires when `enable_custom_operations = true` is set in config. Fires before `generate_custom_module` for the containing module.

### generate_custom_module

```py
def generate_custom_module(self, module: ast.Module) -> ast.Module:
```

Called once per custom operation module (`custom_queries.py` for queries, `custom_mutations.py` for mutations), after all builder methods have been generated. Only fires when `enable_custom_operations = true`. There is no corresponding code-string hook - these files are written directly after AST serialisation. See [Custom operations and fields coverage](./02-custom-plugins.md#custom-operations-and-fields-coverage) for which hooks reach the other custom files.

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

### generate_client_code

```py
def generate_client_code(self, generated_code: str) -> str:
```

Called once with the complete `{client_file_name}.py` source as a string, immediately before the file is written to disk.

### generate_enums_module

```py
def generate_enums_module(self, module: ast.Module) -> ast.Module:
```

Called once, after all enum classes have been generated and collected into the module. Later this module is saved as `{enums_module_name}.py`.

### generate_enums_code

```py
def generate_enums_code(self, generated_code: str) -> str:
```

Called once with the complete `{enums_module_name}.py` source as a string, immediately before the file is written to disk. This is the last point at which the enums file can be modified.

### generate_init_module

```py
def generate_init_module(self, module: ast.Module) -> ast.Module:
```

Called once, after all re-export imports have been added to the init module. Later this module is saved as `__init__.py`.

### generate_init_code

```py
def generate_init_code(self, generated_code: str) -> str:
```

Called once with the complete `__init__.py` source as a string, immediately before the file is written to disk.

