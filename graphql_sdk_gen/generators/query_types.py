import ast
from typing import Union

from graphql import GraphQLSchema, OperationDefinitionNode

from ..exceptions import NotSupported, ParsingError
from .codegen import (
    generate_ann_assign,
    generate_class_def,
    generate_import_from,
    parse_field_type,
)
from .constants import OPTIONAL
from .schema_types import ClassType


class QueryTypesGenerator:
    def __init__(
        self,
        schema: GraphQLSchema,
        fields: dict[str, dict[str, Union[ast.AnnAssign, ast.Assign]]],
        class_types: dict[str, ClassType],
        query: OperationDefinitionNode,
        schema_types_module_name: str,
    ) -> None:
        self.schema = schema
        self.fields = fields
        self.class_types = class_types

        self.query = query
        self.schema_types_module_name = schema_types_module_name

        if not self.query.name:
            raise NotSupported("Queries without name are not supported.")

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

            field_def = generate_ann_assign(
                field.name.value, parse_field_type(field_type.type), lineno
            )
            field_type_name = self._walk_annotation(field_def.annotation)
            field_def.annotation = self._procces_annotation(
                field_def.annotation, field_type_name
            )
            class_def.body.append(field_def)

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
            orginal_field_definition = self.fields[type_name][field_name]

            field_type_name = self._walk_annotation(orginal_field_definition.annotation)
            annotation = self._procces_annotation(
                orginal_field_definition.annotation, field_type_name
            )
            field_def = ast.AnnAssign(
                target=orginal_field_definition.target,
                annotation=annotation,
                simple=1,
                lineno=lineno,
            )
            class_def.body.append(field_def)

            if field.selection_set:
                extra_defs.extend(
                    self._generate_dependency_type_class(
                        field_type_name,
                        field.selection_set,
                    )
                )

        return extra_defs + [class_def]

    def _procces_annotation(self, annotation, field_type_name):
        if (field_type := self.class_types.get(field_type_name)) in (
            ClassType.OBJECT,
            ClassType.INTERFACE,
        ):
            return self._add_prefix_to_annotation(annotation, self.query_name)

        if field_type == ClassType.ENUM:
            self.used_enums.append(field_type_name)

        return annotation

    def _walk_annotation(self, annotation):
        if isinstance(annotation, ast.Name):
            return annotation.id.replace('"', "")

        return self._walk_annotation(annotation.slice)

    def _add_prefix_to_annotation(self, annotation, prefix):
        if isinstance(annotation, ast.Name):
            if annotation.id.startswith('"') and annotation.id.endswith('"'):
                result = '"' + prefix + annotation.id.replace('"', "") + '"'
            else:
                result = prefix + annotation.id
            return ast.Name(id=result)

        if isinstance(annotation, ast.Subscript):
            return ast.Subscript(
                value=annotation.value,
                slice=self._add_prefix_to_annotation(annotation.slice, prefix),
            )

        raise ParsingError("Invalid annotation type.")

    def generate(self) -> ast.Module:
        if self.used_enums:
            self.imports.append(
                generate_import_from(self.used_enums, self.schema_types_module_name, 1)
            )
        return ast.Module(body=self.imports + self.class_defs, type_ignores=[])
