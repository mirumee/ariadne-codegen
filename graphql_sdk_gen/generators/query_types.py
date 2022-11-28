import ast
from typing import Optional, Union

from graphql import (
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    GraphQLField,
    GraphQLSchema,
    OperationDefinitionNode,
    OperationType,
    print_ast,
)

from ..exceptions import NotSupported, ParsingError
from .codegen import (
    generate_ann_assign,
    generate_class_def,
    generate_expr,
    generate_import_from,
    generate_method_call,
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
        enums_module_name: str,
        fragments_definitions: Optional[dict[str, FragmentDefinitionNode]] = None,
    ) -> None:
        self.schema = schema
        self.fields = fields
        self.class_types = class_types

        self.query = query
        self.enums_module_name = enums_module_name
        self.fragments_definitions = (
            fragments_definitions if fragments_definitions else {}
        )

        if not self.query.name:
            raise NotSupported("Queries without name are not supported.")

        self.query_name = self.query.name.value

        self.imports: list[ast.stmt] = [
            generate_import_from([OPTIONAL], "typing"),
            generate_import_from(["BaseModel"], "pydantic"),
        ]

        self.public_names: list[str] = []
        self.class_defs: list = []
        self.used_enums: list = []
        self.used_fragments_names: set[str] = set()

        self._parse_query()

    def _parse_query(self):
        class_def = generate_class_def(self.query_name, ["BaseModel"])
        self.public_names.append(class_def.name)

        extra_defs = []
        for lineno, field in enumerate(
            self._resolve_selection_set(self.query.selection_set), start=1
        ):
            field_type = self._get_field_type_from_schema(field.name.value)
            field_def = generate_ann_assign(
                field.name.value, parse_field_type(field_type.type), lineno=lineno
            )
            field_type_name = self._walk_annotation(field_def.annotation)
            field_def.annotation = self._procces_annotation(
                field_def.annotation, field_type_name
            )
            class_def.body.append(field_def)

            if field.selection_set:
                dependencies_defs = self._generate_dependency_type_class(
                    field_type_name,
                    field.selection_set,
                )
                if dependencies_defs:
                    extra_defs.extend(dependencies_defs)
        self.class_defs.append(class_def)
        self.class_defs.extend(extra_defs)

    def _get_field_type_from_schema(self, name: str) -> GraphQLField:
        if (
            self.query.operation == OperationType.QUERY
            and self.schema.query_type
            and (field_type := self.schema.query_type.fields.get(name))
        ):
            return field_type
        if (
            self.query.operation == OperationType.MUTATION
            and self.schema.mutation_type
            and (field_type := self.schema.mutation_type.fields.get(name))
        ):
            return field_type
        raise ParsingError(f"Definition for {name} not found in schema.")

    def _generate_dependency_type_class(self, type_name, selection_set):
        class_def = generate_class_def(self.query_name + type_name, ["BaseModel"])
        if class_def.name in self.public_names:
            return None
        self.public_names.append(class_def.name)

        extra_defs = []
        for lineno, field in enumerate(
            self._resolve_selection_set(selection_set), start=1
        ):
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
                dependencies_defs = self._generate_dependency_type_class(
                    field_type_name,
                    field.selection_set,
                )
                if dependencies_defs:
                    extra_defs.extend(dependencies_defs)

        return [class_def] + extra_defs

    def _resolve_selection_set(self, selection_set):
        fields = []
        for selection in selection_set.selections:
            if isinstance(selection, FieldNode):
                fields.append(selection)
            elif isinstance(selection, FragmentSpreadNode):
                self.used_fragments_names.add(selection.name.value)
                fields.extend(
                    self._resolve_selection_set(
                        self.fragments_definitions[selection.name.value].selection_set
                    )
                )
        return fields

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
                generate_import_from(self.used_enums, self.enums_module_name, 1)
            )
        return ast.Module(
            body=self.imports
            + self.class_defs
            + [
                generate_expr(
                    generate_method_call(class_def.name, "update_forward_refs")
                )
                for class_def in self.class_defs
            ],
            type_ignores=[],
        )

    def get_operation_as_str(self) -> str:
        operation_str = print_ast(self.query)

        if self.used_fragments_names:
            operation_str += "\n\n" + "\n\n".join(
                {
                    print_ast(self.fragments_definitions[n])
                    for n in self.used_fragments_names
                }
            )

        return operation_str
