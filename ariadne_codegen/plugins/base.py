import ast
from typing import Dict

from graphql import GraphQLSchema


class Plugin:
    def __init__(self, schema: GraphQLSchema, config_dict: Dict) -> None:
        self.schema = schema
        self.config_dict = config_dict

    def generate_init_module(self, module: ast.Module) -> ast.Module:
        return module
