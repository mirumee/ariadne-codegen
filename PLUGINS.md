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



## Example

This example plugin adds `__version__ = "..."` to generated `__init__.py` file.

```py
import ast

from ariadne_codegen.plugins.base import Plugin


class VersionPlugin(Plugin):
    def generate_init_module(self, module: ast.Module) -> ast.Module:
        version = (
            self.config_dict.get("tools", {})
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
[tools.version_plugin]
version = 0.21
``` 
