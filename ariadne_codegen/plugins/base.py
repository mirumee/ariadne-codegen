import ast
from typing import Optional

from graphql import GraphQLSchema


class Plugin:
    def __init__(self, schema: Optional[GraphQLSchema] = None) -> None:
        self.schema = schema

    def generate_init_module(self, module: ast.Module) -> ast.Module:
        return module
