import ast
from typing import Dict, List, Optional, Type

from graphql import GraphQLSchema

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
