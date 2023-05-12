# Plugins

## How to implement plugin

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


## Hooks

### generate_init_module

```py
def generate_init_module(self, module: ast.Module) -> ast.Module:
```

Hook executed on generation of init module. Module has list of public, generated classes and reimports them all. Later this module will be saved as `__init__.py`.

### generate_init_import

```py
def generate_init_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
```

Hook executed on addition of import to init module. Later this import will be placed in `__init__.py`.

### generate_enum

```py
def generate_enum(self, class_def: ast.ClassDef, enum_type: GraphQLEnumType) -> ast.ClassDef:
```

Hook executed on generation of class definition of single enum.

### generate_enums_module

```py
def generate_enums_module(self, module: ast.Module) -> ast.Module:
```

Hook executed on generation of enums module. Module has all classes representing enums from schema. Later this module will be saved as `{enums_module_name}.py`, `enums_module_name` is taken from config.

### generate_client_module

```py
def generate_client_module(self, module: ast.Module) -> ast.Module:
```

Hook executed on generation of client module. Module contains `gql` function definition and client class. Later this module will be saved as `{client_file_name}.py`, `client_file_name` is taken from config.

### generate_gql_function

```py
def generate_gql_function(self, function_def: ast.FunctionDef) -> ast.FunctionDef:
```

Hook executed on generation of `gql` function.

### generate_client_class

```py
def generate_client_class(self, class_def: ast.ClassDef) -> ast.ClassDef:
```

Hook executed on generation of client class. Class contains method for every graphql operation.

### generate_client_import

```py
def generate_client_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
```

Hook executed on addition of import to client module. Later this import will be placed in `{client_file_name}.py`, `client_file_name` is taken from config.

### generate_client_method

```py
def generate_client_method(
        self, method_def: Union[ast.FunctionDef, ast.AsyncFunctionDef]
) -> Union[ast.FunctionDef, ast.AsyncFunctionDef]:
```

Hook executed on generation of client's method, which represents single graphql operation. Depends on the configuration method can be either async or not.
`
### generate_arguments

```py
def generate_arguments(
    self,
    arguments: ast.arguments,
    variable_definitions: Tuple[VariableDefinitionNode, ...],
) -> ast.arguments:
```

Hook executed on generation of arguments for specific client's method.

### generate_arguments_dict

```py
def generate_arguments_dict(
    self,
    dict_: ast.Dict,
    variable_definitions: Tuple[VariableDefinitionNode, ...],
) -> ast.Dict:
```

Hook executed on generation of dictionary with arguments of graphql operation. Serialized dictionary is later used as variables payload.

### generate_inputs_module

```py
def generate_inputs_module(self, module: ast.Module) -> ast.Module:
```

Hook executed on generation of inputs module. Module has all classes representing inputs from schema. Later this module will be saved as `{input_types_module_name}.py`, `input_types_module_name` is taken from config.

### generate_input_class

```py
def generate_input_class(
    self, class_def: ast.ClassDef, input_type: GraphQLInputObjectType
) -> ast.ClassDef:
```

Hook executed on generation of class definition for input from schema.

### generate_input_field

```py
    def generate_input_field(
        self,
        field_implementation: ast.AnnAssign,
        input_field: GraphQLInputField,
        field_name: str,
    ) -> ast.AnnAssign:
```

Hook executed on generation of representation for input field.

### generate_result_types_module

```py
def generate_result_types_module(
    self, module: ast.Module, operation_definition: ExecutableDefinitionNode
) -> ast.Module:
```

Hook executed on generation of module with models reprenting result of given operation.

### generate_operation_str

```py
def generate_operation_str(
    self, operation_str: str, operation_definition: ExecutableDefinitionNode
) -> str:
```

Hook executed on generation of string representation of given operation. Result is later used by generated client as part of payload sent to graphql server.

### generate_result_class

```py
def generate_result_class(
    self,
    class_def: ast.ClassDef,
    operation_definition: ExecutableDefinitionNode,
    selection_set: SelectionSetNode,
) -> ast.ClassDef:
```

Hook executed on generation of single model, part of result of given query or mutation. 


### generate_result_field

```py
def generate_result_field(
    self,
    field_implementation: ast.AnnAssign,
    operation_definition: ExecutableDefinitionNode,
    field: FieldNode,
) -> ast.AnnAssign:
```

Hook executed on generation of single model field.

### generate_scalars_module

```py
def generate_scalars_module(self, module: ast.Module) -> ast.Module:
```

Hook executed on generation of module with mappings for custom scalars. Later is saved as `scalars.py`.

### generate_scalars_parse_dict

```py
def generate_scalars_parse_dict(self, dict_: ast.Dict) -> ast.Dict:
```

Hook executed on generation of dictionary with custom scalars parse methods.

### generate_scalars_serialize_dict

```py
def generate_scalars_serialize_dict(self, dict_: ast.Dict) -> ast.Dict:
```

Hook executed on generation of dictionary with custom scalars serialize methods.

### generate_client_code

```py
def generate_client_code(self, generated_code: str) -> str:
```

Hook executed on generation of client code. Result is used as content of `{client_file_name}.py`, `client_file_name` is taken from config.

### generate_enums_code

```py
def generate_enums_code(self, generated_code: str) -> str:
```

Hook executed on generation of enums code. Result is used as content of `{enums_module_name}.py`, `enums_module_name` is taken from config.

### generate_inputs_code

```py
def generate_inputs_code(self, generated_code: str) -> str:
```

Hook executed on generation of input models code. Result is used as content of `{input_types_module_name}.py`, `input_types_module_name` is taken from config.

### generate_result_types_code

```py    
def generate_result_types_code(self, generated_code: str) -> str:
```

Hook executed on generation of result models code for one operation. Result is used as content of `{operation_name}.py`.

### copy_code

```py
def copy_code(self, copied_code: str) -> str:
```

Hook executed on coping file's content to result package.
Files hook is called for:
- `base_client.py` or `async_base_client.py` or custom base client `base_client_file_path`
- `base_model.py`
- `exceptions.py`
- all files from config's `files_to_include`

### generate_scalars_code

```py
def generate_scalars_code(self, generated_code: str) -> str:
```

Hook executed on generation of scalars mappings code. Result is used as content of `scalars.py`.

### generate_init_code

```py
def generate_init_code(self, generated_code: str) -> str:
```

Hook executed on generation of init code. Result is used as content of `__init__.py`.

### process_name

```py
def process_name(self, name: str, node: Optional[Node] = None) -> str:
```

Hook executed on processing of GraphQL field, argument or operation name.

### generate_fragments_module

```py
def generate_fragments_module(
    self,
    module: ast.Module,
    fragments_definitions: Dict[str, FragmentDefinitionNode],
) -> ast.Module:
```

Hook executed on generation of fragments module. Module has classes representing all fragments from provided queries. Later this module will be saved as `{fragments_module_name}.py`, `fragments_module_name` is taken from config.


## Example

This example plugin adds `__version__ = "..."` to generated `__init__.py` file.

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

`VersionPlugin` reads version from parsed `pyproject.toml`, eg. following entry will produce `__version__ = "0.21"`.

```toml
[tool.version_plugin]
version = 0.21
```
