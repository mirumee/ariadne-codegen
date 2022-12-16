import ast
from typing import cast

from graphql import GraphQLEnumType, GraphQLSchema

from .codegen import (
    generate_assign,
    generate_class_def,
    generate_constant,
    generate_import_from,
    generate_module,
)
from .constants import ENUM_CLASS, ENUM_MODULE


class EnumsGenerator:
    def __init__(self, schema: GraphQLSchema) -> None:
        self.schema = schema

        self._imports: list[ast.ImportFrom] = [
            generate_import_from([ENUM_CLASS], ENUM_MODULE)
        ]
        self._class_defs: list[ast.ClassDef] = [
            self._parse_enum_definition(d) for d in self._filter_enum_types()
        ]

    def generate(self) -> ast.Module:
        module_body = cast(list[ast.stmt], self._imports) + cast(
            list[ast.stmt], self._class_defs
        )

        return generate_module(body=module_body)

    def get_generated_public_names(self) -> list[str]:
        return [c.name for c in self._class_defs]

    def _filter_enum_types(self) -> list[GraphQLEnumType]:
        return [
            definition
            for name, definition in self.schema.type_map.items()
            if isinstance(definition, GraphQLEnumType) and not name.startswith("__")
        ]

    def _parse_enum_definition(self, definition: GraphQLEnumType) -> ast.ClassDef:
        fields = [
            generate_assign([val_name], generate_constant(val_def.value), lineno)
            for lineno, (val_name, val_def) in enumerate(
                definition.values.items(), start=1
            )
        ]

        return generate_class_def(
            name=definition.name,
            base_names=["str", ENUM_CLASS],
            body=cast(list[ast.stmt], fields),
        )
