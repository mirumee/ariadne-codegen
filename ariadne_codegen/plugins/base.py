import ast

from graphql import GraphQLSchema


class BasePlugin:
    def __init__(self, schema: GraphQLSchema) -> None:
        self.schema = schema

    def generate_init_file(self, module: ast.Module) -> ast.Module:
        return module
