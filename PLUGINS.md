# Plugins

## How to implement plugin

Plugin is a class which inherits from `ariadne_codegen.plugins.base.Plugin`. Plugin's instance is created once, at the beginning of `ariadne-codegen` command, with following arguments:
- `schema: GraphQLSchema`: parsed graphql schema
- `config_dict: Dict`: parsed `pyproject.toml` file represented as a dictionary

To handle specific hooks class needs to override [base methods](#hooks). Not changed methods have no effect on generated code and don't raise `NotImplementedError`.


## Plugins lookup

Plugin can be provided to `ariadne-codegen` in 2 ways:

1. Providing full import path to class, eg. `my_package.my_plugins.MyPlugin`.

2. Providing only package name, eg. `my_package`. In this case all plugins from selected package will be used. For class to be accessible this way, it needs to be in package's public api. Plugin has to be importable from package, eg. `from my_package import MyPlugin` has to work.


## Hooks

### generate_init_module

```py
def generate_init_module(self, module: ast.Module) -> ast.Module:
```

Hook which is executed after generation of init module. Module has list of public, generated classes and reimports them all. Later this module will be saved as `__init__.py`
