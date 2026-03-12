import ast
from typing import Optional, cast
from warnings import warn

from graphql import GraphQLEnumType, GraphQLSchema

from ..codegen import (
    generate_assign,
    generate_class_def,
    generate_constant,
    generate_import_from,
    generate_module,
)
from ..plugins.manager import PluginManager
from ..utils import process_name
from .constants import ENUM_CLASS, ENUM_MODULE


class EnumsGenerator:
    def __init__(
        self, schema: GraphQLSchema, plugin_manager: Optional[PluginManager] = None
    ) -> None:
        self.schema = schema
        self.plugin_manager = plugin_manager

        self._generated_public_names: list[str] = []
        self._imports: list[ast.ImportFrom] = [
            generate_import_from([ENUM_CLASS], ENUM_MODULE)
        ]
        self._class_defs: list[ast.ClassDef] = [
            self._parse_enum_definition(d) for d in self._filter_enum_types()
        ]

    def generate(self, types_to_include: Optional[list[str]] = None) -> ast.Module:
        class_defs = self._filter_class_defs(types_to_include)
        self._generated_public_names = [class_def.name for class_def in class_defs]

        module = generate_module(
            body=cast(list[ast.stmt], self._imports) + cast(list[ast.stmt], class_defs)
        )

        if self.plugin_manager:
            module = self.plugin_manager.generate_enums_module(module)

        return module

    def get_generated_public_names(self) -> list[str]:
        return self._generated_public_names

    def _filter_enum_types(self) -> list[GraphQLEnumType]:
        return [
            definition
            for name, definition in self.schema.type_map.items()
            if isinstance(definition, GraphQLEnumType) and not name.startswith("__")
        ]

    def _parse_enum_definition(self, definition: GraphQLEnumType) -> ast.ClassDef:
        fields: list[ast.stmt] = []
        for lineno, (val_name, val_def) in enumerate(
            definition.values.items(), start=1
        ):
            if val_def.deprecation_reason:
                warn(
                    f"Enum value '{val_name}' on enum '{definition.name}' is "
                    f"deprecated: {val_def.deprecation_reason}",
                    DeprecationWarning,
                    stacklevel=2,
                )
            name = process_name(
                val_name,
                convert_to_snake_case=False,
                plugin_manager=self.plugin_manager,
            )
            fields.append(
                generate_assign([name], generate_constant(val_def.value), lineno)
            )

        class_def = generate_class_def(
            name=definition.name,
            base_names=["str", ENUM_CLASS],
            body=cast(list[ast.stmt], fields),
        )
        if self.plugin_manager:
            class_def = self.plugin_manager.generate_enum(class_def, definition)
        return class_def

    def _filter_class_defs(
        self, types_to_include: Optional[list[str]] = None
    ) -> list[ast.ClassDef]:
        if types_to_include is None:
            return self._class_defs

        return [
            class_def
            for class_def in self._class_defs
            if class_def.name in types_to_include
        ]
