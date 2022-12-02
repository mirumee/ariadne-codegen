import ast
from itertools import chain
from typing import Optional, Union, cast

from graphql import (
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    GraphQLField,
    GraphQLSchema,
    InlineFragmentNode,
    NameNode,
    OperationDefinitionNode,
    OperationType,
    SelectionNode,
    SelectionSetNode,
    print_ast,
)

from ..exceptions import NotSupported, ParsingError
from .codegen import (
    generate_ann_assign,
    generate_class_def,
    generate_expr,
    generate_import_from,
    generate_method_call,
    generate_module,
    generate_name,
    generate_subscript,
    generate_tuple,
    generate_typename_field_definition,
    parse_field_type,
)
from .constants import (
    BASE_MODEL_CLASS_NAME,
    FIELD_CLASS,
    OPTIONAL,
    PYDANTIC_MODULE,
    TYPENAME_FIELD_NAME,
    TYPING_MODULE,
    UNION,
    UPDATE_FORWARD_REFS_METHOD,
)
from .schema_types import ClassType
from .types import Annotation, AnnotationSlice, GraphQLFieldType


class ResultTypesGenerator:
    def __init__(
        self,
        schema: GraphQLSchema,
        operation_definition: OperationDefinitionNode,
        schema_fields_implementations: dict[str, dict[str, ast.AnnAssign]],
        class_types: dict[str, ClassType],
        enums_module_name: str,
        fragments_definitions: Optional[dict[str, FragmentDefinitionNode]] = None,
        base_model_import: Optional[ast.ImportFrom] = None,
    ) -> None:
        self.schema = schema
        self.schema_fields_implementations = schema_fields_implementations
        self.class_types = class_types

        self.operation_definition = operation_definition
        if not self.operation_definition.name:
            raise NotSupported("Operations without name are not supported.")
        self.operation_name = self.operation_definition.name.value

        self.enums_module_name = enums_module_name
        self.fragments_definitions = (
            fragments_definitions if fragments_definitions else {}
        )

        self._imports: list[ast.ImportFrom] = [
            generate_import_from([OPTIONAL, UNION], TYPING_MODULE),
            generate_import_from([FIELD_CLASS], PYDANTIC_MODULE),
            base_model_import
            or generate_import_from([BASE_MODEL_CLASS_NAME], PYDANTIC_MODULE),
        ]

        self._public_names: list[str] = []
        self._class_defs: list[ast.ClassDef] = []
        self._used_enums: list[str] = []
        self._used_fragments_names: set[str] = set()

        self._parse_operation_definition()

    def generate(self) -> ast.Module:
        if self._used_enums:
            self._imports.append(
                generate_import_from(self._used_enums, self.enums_module_name, 1)
            )
        update_forward_refs_calls = [
            generate_expr(
                generate_method_call(class_def.name, UPDATE_FORWARD_REFS_METHOD)
            )
            for class_def in self._class_defs
        ]
        module_body = (
            cast(list[ast.stmt], self._imports)
            + cast(list[ast.stmt], self._class_defs)
            + cast(list[ast.stmt], update_forward_refs_calls)
        )

        return generate_module(module_body)

    def get_operation_as_str(self) -> str:
        operation_str = print_ast(self.operation_definition)
        if self._used_fragments_names:
            operation_str += "\n\n" + "\n\n".join(
                {
                    print_ast(self.fragments_definitions[n])
                    for n in self._used_fragments_names
                }
            )

        return operation_str

    def get_generated_public_names(self) -> list[str]:
        return self._public_names

    def _parse_operation_definition(self):
        class_def = generate_class_def(self.operation_name, [BASE_MODEL_CLASS_NAME])
        self._public_names.append(class_def.name)

        extra_classes = []
        for lineno, field in enumerate(
            self._resolve_selection_set(self.operation_definition.selection_set),
            start=1,
        ):
            schema_field = self._get_field_from_schema(field.name.value)
            field_implementation = generate_ann_assign(
                field.name.value,
                parse_field_type(cast(GraphQLFieldType, schema_field.type)),
                lineno=lineno,
            )

            field_types_names = self._get_field_types_names(
                cast(Annotation, field_implementation.annotation)
            )
            field_implementation.annotation = self._procces_annotation(
                cast(Annotation, field_implementation.annotation), field_types_names
            )

            class_def.body.append(field_implementation)

            extra_classes.extend(
                self._parse_field_selection_set_types(
                    field.selection_set, field_types_names
                )
            )

        self._class_defs.append(class_def)
        self._class_defs.extend(extra_classes)

    def _resolve_selection_set(
        self, selection_set: SelectionSetNode, root_type: str = ""
    ) -> list[FieldNode]:
        fields = []
        for selection in selection_set.selections:
            if isinstance(selection, FieldNode):
                fields.append(selection)
            elif isinstance(selection, FragmentSpreadNode):
                self._used_fragments_names.add(selection.name.value)
                fields.extend(
                    self._resolve_selection_set(
                        self.fragments_definitions[selection.name.value].selection_set,
                        root_type,
                    )
                )
            elif isinstance(selection, InlineFragmentNode):
                if selection.type_condition.name.value == root_type:
                    fields.extend(
                        self._resolve_selection_set(selection.selection_set, root_type)
                    )
        return fields

    def _get_field_from_schema(self, name: str) -> GraphQLField:
        if (
            self.operation_definition.operation == OperationType.QUERY
            and self.schema.query_type
            and (field := self.schema.query_type.fields.get(name))
        ):
            return field
        if (
            self.operation_definition.operation == OperationType.MUTATION
            and self.schema.mutation_type
            and (field := self.schema.mutation_type.fields.get(name))
        ):
            return field
        raise ParsingError(f"Definition for {name} not found in schema.")

    def _get_field_types_names(
        self, annotation: Union[Annotation, AnnotationSlice]
    ) -> list[str]:
        if isinstance(annotation, ast.Name):
            return [annotation.id.replace('"', "")]

        if isinstance(annotation, ast.Subscript):
            if isinstance(annotation.slice, ast.Tuple):
                return list(
                    chain(
                        *[
                            self._get_field_types_names(cast(AnnotationSlice, elt))
                            for elt in annotation.slice.elts
                        ]
                    )
                )
            return self._get_field_types_names(cast(AnnotationSlice, annotation.slice))
        return []

    def _procces_annotation(
        self, annotation: Annotation, field_type_names: list[str]
    ) -> Annotation:
        if any(
            self.class_types.get(field_type_name)
            in (
                ClassType.OBJECT,
                ClassType.INTERFACE,
            )
            for field_type_name in field_type_names
        ):
            return self._add_prefix_to_annotation(annotation, self.operation_name)

        for field_type_name in field_type_names:
            if self.class_types.get(field_type_name) == ClassType.ENUM:
                self._used_enums.append(field_type_name)

        return annotation

    def _add_prefix_to_annotation(
        self, annotation: AnnotationSlice, prefix: str
    ) -> Annotation:
        if isinstance(annotation, ast.Name):
            if annotation.id.startswith('"') and annotation.id.endswith('"'):
                return generate_name(
                    '"' + prefix + annotation.id.replace('"', "") + '"'
                )

        if isinstance(annotation, ast.Subscript):
            if isinstance(annotation.slice, ast.Tuple):
                return generate_subscript(
                    value=annotation.value,
                    slice_=generate_tuple(
                        [
                            self._add_prefix_to_annotation(
                                cast(AnnotationSlice, elt), prefix
                            )
                            for elt in annotation.slice.elts
                        ]
                    ),
                )

            return generate_subscript(
                value=annotation.value,
                slice_=self._add_prefix_to_annotation(
                    cast(AnnotationSlice, annotation.slice), prefix
                ),
            )

        raise ParsingError("Invalid annotation type.")

    def _parse_field_selection_set_types(
        self, selection_set: Optional[SelectionSetNode], field_types_names: list[str]
    ) -> list[ast.ClassDef]:
        if selection_set:
            generated_classes = []
            add_typename = len(field_types_names) > 1
            for field_type_name in field_types_names:
                generated_classes.extend(
                    self._generate_classes_for_type(
                        field_type_name, selection_set, add_typename
                    )
                )
            return generated_classes
        return []

    def _generate_classes_for_type(
        self,
        type_name: str,
        selection_set: SelectionSetNode,
        add_typename: bool = False,
    ) -> list[ast.ClassDef]:
        class_def = generate_class_def(
            self.operation_name + type_name, [BASE_MODEL_CLASS_NAME]
        )
        if class_def.name in self._public_names:
            return []
        self._public_names.append(class_def.name)

        extra_classes = []
        resolved_selection_set = self._resolve_selection_set(selection_set, type_name)
        if add_typename:
            (
                resolved_selection_set,
                selection_set.selections,
            ) = self._add_typename_field_to_selections(
                resolved_selection_set, selection_set
            )

        for lineno, field in enumerate(resolved_selection_set, start=1):
            field_name = field.name.value
            schema_field_implementation = self._get_schema_field_implementation(
                type_name, field_name
            )

            field_type_names = self._get_field_types_names(
                cast(Annotation, schema_field_implementation.annotation)
            )
            field_implementation = generate_ann_assign(
                target=schema_field_implementation.target,
                annotation=self._procces_annotation(
                    cast(Annotation, schema_field_implementation.annotation),
                    field_type_names,
                ),
                value=schema_field_implementation.value,
                lineno=lineno,
            )
            class_def.body.append(field_implementation)

            extra_classes.extend(
                self._parse_field_selection_set_types(
                    field.selection_set, field_type_names
                )
            )

        return [class_def] + extra_classes

    def _get_schema_field_implementation(
        self, type_name: str, field_name: str
    ) -> ast.AnnAssign:
        if field_name == TYPENAME_FIELD_NAME:
            return generate_typename_field_definition()
        return cast(
            ast.AnnAssign, self.schema_fields_implementations[type_name][field_name]
        )

    def _add_typename_field_to_selections(
        self, resolved_fields: list[FieldNode], selection_set: SelectionSetNode
    ) -> tuple[list[FieldNode], tuple[SelectionNode, ...]]:
        field_names = {f.name.value for f in resolved_fields}
        if TYPENAME_FIELD_NAME not in field_names:
            typename_field = FieldNode(name=NameNode(value=TYPENAME_FIELD_NAME))
            return [typename_field, *resolved_fields], (
                typename_field,
                *selection_set.selections,
            )
        return resolved_fields, selection_set.selections
