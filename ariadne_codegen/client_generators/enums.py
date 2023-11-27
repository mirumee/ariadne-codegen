import ast
from keyword import iskeyword
from typing import List, Optional, cast

from graphql import GraphQLEnumType, GraphQLSchema

from ..codegen import (
    generate_assign,
    generate_class_def,
    generate_constant,
    generate_import_from,
    generate_module,
)
from ..plugins.manager import PluginManager
from .constants import ENUM_CLASS, ENUM_MODULE


class EnumsGenerator:
    def __init__(
        self, schema: GraphQLSchema, plugin_manager: Optional[PluginManager] = None
    ) -> None:
        self.schema = schema
        self.plugin_manager = plugin_manager

        self._generated_public_names: List[str] = []
        self._imports: List[ast.ImportFrom] = [
            generate_import_from([ENUM_CLASS], ENUM_MODULE)
        ]
        self._class_defs: List[ast.ClassDef] = [
            self._parse_enum_definition(d) for d in self._filter_enum_types()
        ]

    def generate(self, types_to_include: Optional[List[str]] = None) -> ast.Module:
        class_defs = self._filter_class_defs(types_to_include)
        self._generated_public_names = [class_def.name for class_def in class_defs]

        module = generate_module(
            body=cast(List[ast.stmt], self._imports) + cast(List[ast.stmt], class_defs)
        )

        if self.plugin_manager:
            module = self.plugin_manager.generate_enums_module(module)

        return module

    def get_generated_public_names(self) -> List[str]:
        return self._generated_public_names

    def _filter_enum_types(self) -> List[GraphQLEnumType]:
        return [
            definition
            for name, definition in self.schema.type_map.items()
            if isinstance(definition, GraphQLEnumType) and not name.startswith("__")
        ]

    def _parse_enum_definition(self, definition: GraphQLEnumType) -> ast.ClassDef:
        fields: List[ast.stmt] = []
        for lineno, (val_name, val_def) in enumerate(
            definition.values.items(), start=1
        ):
            name = val_name if not iskeyword(val_name) else val_name + "_"
            fields.append(
                generate_assign([name], generate_constant(val_def.value), lineno)
            )

        class_def = generate_class_def(
            name=definition.name,
            base_names=["str", ENUM_CLASS],
            body=cast(List[ast.stmt], fields),
        )
        if self.plugin_manager:
            class_def = self.plugin_manager.generate_enum(class_def, definition)
        return class_def

    def _filter_class_defs(
        self, types_to_include: Optional[List[str]] = None
    ) -> List[ast.ClassDef]:
        if types_to_include is None:
            return self._class_defs

        return [
            class_def
            for class_def in self._class_defs
            if class_def.name in types_to_include
        ]
