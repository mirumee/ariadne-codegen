import ast

from graphql import GraphQLSchema


class Plugin:
    def __init__(self, schema: GraphQLSchema) -> None:
        self.schema = schema

    def generate_init_module(self, module: ast.Module) -> ast.Module:
        return module
