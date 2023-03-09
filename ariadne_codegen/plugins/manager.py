import ast
from typing import Dict, List, Optional, Type, Union

from graphql import GraphQLEnumType, GraphQLSchema

from .base import Plugin


class PluginManager:
    def __init__(
        self,
        schema: GraphQLSchema,
        config_dict: Optional[Dict] = None,
        plugins_types: Optional[List[Type[Plugin]]] = None,
    ) -> None:

        self.plugins: List[Plugin] = [
            cls(schema=schema, config_dict=config_dict or {})
            for cls in plugins_types or []
        ]

    def generate_init_module(self, module: ast.Module) -> ast.Module:
        modified_module = module
        for plugin in self.plugins:
            modified_module = plugin.generate_init_module(modified_module)
        return modified_module

    def generate_init_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
        modified_import = import_
        for plugin in self.plugins:
            modified_import = plugin.generate_init_import(modified_import)
        return modified_import

    def generate_enum(
        self, class_def: ast.ClassDef, enum_type: GraphQLEnumType
    ) -> ast.ClassDef:
        modified_class = class_def
        for plugin in self.plugins:
            modified_class = plugin.generate_enum(modified_class, enum_type=enum_type)
        return modified_class

    def generate_enums_module(self, module: ast.Module) -> ast.Module:
        modified_module = module
        for plugin in self.plugins:
            modified_module = plugin.generate_init_module(modified_module)
        return modified_module

    def generate_client_module(self, module: ast.Module) -> ast.Module:
        modified_module = module
        for plugin in self.plugins:
            modified_module = plugin.generate_client_module(modified_module)
        return modified_module

    def generate_gql_function(self, function_def: ast.FunctionDef) -> ast.FunctionDef:
        modified_function = function_def
        for plugin in self.plugins:
            modified_function = plugin.generate_gql_function(modified_function)
        return modified_function

    def generate_client_class(self, class_def: ast.ClassDef) -> ast.ClassDef:
        modified_class = class_def
        for plugin in self.plugins:
            modified_class = plugin.generate_client_class(modified_class)
        return modified_class

    def generate_client_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
        modified_import = import_
        for plugin in self.plugins:
            modified_import = plugin.generate_client_import(modified_import)
        return modified_import

    def generate_client_method(
        self, method_def: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> Union[ast.FunctionDef, ast.AsyncFunctionDef]:
        modified_method = method_def
        for plugin in self.plugins:
            modified_method = plugin.generate_client_method(modified_method)
        return modified_method
