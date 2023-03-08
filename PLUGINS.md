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

Hook executed on generation of init module. Module has list of public, generated classes and reimports them all. Later this module will be saved as `__init__.p


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
