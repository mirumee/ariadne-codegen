import ast
from typing import Dict, Tuple, Union

from graphql import GraphQLEnumType, GraphQLSchema, VariableDefinitionNode


class Plugin:
    def __init__(self, schema: GraphQLSchema, config_dict: Dict) -> None:
        self.schema = schema
        self.config_dict = config_dict

    def generate_init_module(self, module: ast.Module) -> ast.Module:
        return module

    def generate_init_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
        return import_

    def generate_enum(
        self, class_def: ast.ClassDef, enum_type: GraphQLEnumType
    ) -> ast.ClassDef:
        return class_def

    def generate_enums_module(self, module: ast.Module) -> ast.Module:
        return module

    def generate_client_module(self, module: ast.Module) -> ast.Module:
        return module

    def generate_gql_function(self, function_def: ast.FunctionDef) -> ast.FunctionDef:
        return function_def

    def generate_client_class(self, class_def: ast.ClassDef) -> ast.ClassDef:
        return class_def

    def generate_client_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
        return import_

    def generate_client_method(
        self, method_def: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> Union[ast.FunctionDef, ast.AsyncFunctionDef]:
        return method_def

    def generate_arguments(
        self,
        arguments: ast.arguments,
        variable_definitions: Tuple[VariableDefinitionNode, ...],
    ) -> ast.arguments:
        return arguments

    def generate_arguments_dict(
        self,
        dict_: ast.Dict,
        variable_definitions: Tuple[VariableDefinitionNode, ...],
    ) -> ast.Dict:
        return dict_
