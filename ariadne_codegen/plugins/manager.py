import ast
from typing import List, Optional

from graphql import GraphQLSchema

from .base import BasePlugin


class PluginsManager:
    def __init__(
        self,
        schema: Optional[GraphQLSchema] = None,
        plugins_classes: Optional[List[type]] = None,
    ) -> None:
        self.plugins: List[BasePlugin] = [cls(schema) for cls in plugins_classes or []]

    def generate_init_module(self, module: ast.Module) -> ast.Module:
        modified_module = module
        for plugin in self.plugins:
            modified_module = plugin.generate_init_module(modified_module)
        return modified_module
