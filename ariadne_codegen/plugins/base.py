import ast
from typing import Dict

from graphql import GraphQLEnumType, GraphQLSchema


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

