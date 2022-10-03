import ast
from typing import Union

from graphql import GraphQLSchema, OperationDefinitionNode

from .base_types import FieldType
from .constants import OPTIONAL
from .utils import (
    add_prefix_to_annotation,
    generate_class_def,
    generate_import_from,
    parse_field_type,
    walk_annotation,
)


class QueryTypesGenerator:
    def __init__(
        self,
        schema: GraphQLSchema,
        fields_definitions: dict[str, dict[str, Union[ast.AnnAssign, ast.Assign]]],
        fields_types: dict[str, FieldType],
        query: OperationDefinitionNode,
        schema_types_module_name: str,
    ) -> None:
        self.schema = schema
        self.fields_definitions = fields_definitions
        self.fields_types = fields_types
        self.query = query
        self.schema_types_module_name = schema_types_module_name

        if not self.query.name:
            raise Exception

        self.query_name = self.query.name.value

        self.imports = [
            generate_import_from([OPTIONAL], "typing"),
            generate_import_from(["BaseModel"], "pydantic"),
        ]

        self.public_names: list[str] = []
        self.class_defs: list = []
        self.used_enums: list = []

        self._parse_query()

    def _parse_query(self):
        class_def = generate_class_def(self.query_name, ["BaseModel"])
        self.public_names.append(class_def.name)

        for lineno, field in enumerate(self.query.selection_set.selections, start=1):
            field_type = self.schema.query_type.fields[field.name.value]

            field_definition = ast.AnnAssign(
                target=ast.Name(id=field.name.value),
                annotation=parse_field_type(field_type.type),
                simple=1,
                lineno=lineno,
            )
            field_type_name = walk_annotation(field_definition.annotation)
            field_definition.annotation = self._procces_annotation(
                field_definition.annotation, field_type_name
            )
            class_def.body.append(field_definition)
            if field.selection_set:
                self.class_defs.extend(
                    self._generate_dependency_type_class(
                        field_type_name,
                        field.selection_set,
                    )
                )
            self.class_defs.append(class_def)

    def _generate_dependency_type_class(self, type_name, selection_set):
        class_def = generate_class_def(self.query_name + type_name, ["BaseModel"])
        self.public_names.append(class_def.name)

        extra_defs = []
        for lineno, field in enumerate(selection_set.selections, start=1):
            field_name = field.name.value
            field_definition = self.fields_definitions[type_name][field_name]
            field_definition.lineno = lineno
            field_type_name = walk_annotation(field_definition.annotation)
            field_definition.annotation = self._procces_annotation(
                field_definition.annotation, field_type_name
            )
            class_def.body.append(field_definition)

            if field.selection_set:
                extra_defs.extend(
                    self._generate_dependency_type_class(
                        field_type_name,
                        field.selection_set,
                    )
                )

        return extra_defs + [class_def]

    def _procces_annotation(self, annotation, field_type_name):
        if (field_type := self.fields_types.get(field_type_name)) == FieldType.OBJECT:
            return add_prefix_to_annotation(annotation, self.query_name)
        elif field_type == FieldType.ENUM:
            self.used_enums.append(field_type_name)
        return annotation

    def generate(self) -> ast.Module:
        if self.used_enums:
            self.imports.append(
                generate_import_from(self.used_enums, self.schema_types_module_name, 1)
            )
        return ast.Module(body=self.imports + self.class_defs, type_ignores=[])
