import ast
from collections import namedtuple
from typing import Optional, Tuple, cast

from graphql import (
    DirectiveNode,
    GraphQLEnumType,
    GraphQLInterfaceType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLUnionType,
)

from ..exceptions import ParsingError
from .codegen import (
    generate_annotation_name,
    generate_list_annotation,
    generate_nullable_annotation,
    generate_union_annotation,
)
from .constants import (
    ANY,
    INCLUDE_DIRECTIVE_NAME,
    OPTIONAL,
    SIMPLE_TYPE_MAP,
    SKIP_DIRECTIVE_NAME,
)
from .types import Annotation, CodegenResultFieldType

FieldNames = namedtuple("FieldNames", ["class_name", "type_name"])


def parse_operation_field(
    type_: CodegenResultFieldType,
    directives: Optional[Tuple[DirectiveNode, ...]] = None,
    class_name: str = "",
) -> Tuple[Annotation, list[FieldNames]]:
    annotation, field_types_names = parse_operation_field_type(
        type_=type_, class_name=class_name
    )
    if not (is_nullable(annotation)) and directives:
        nullable_directives = [INCLUDE_DIRECTIVE_NAME, SKIP_DIRECTIVE_NAME]
        directives_names = [d.name.value for d in directives]
        if any(n in nullable_directives for n in directives_names):
            annotation = generate_nullable_annotation(annotation)
    return annotation, field_types_names


def parse_operation_field_type(
    type_: CodegenResultFieldType,
    nullable: bool = True,
    class_name: str = "",
    add_type_name: bool = False,
) -> Tuple[Annotation, list[FieldNames]]:
    """Parse graphql type and return generated annotation."""
    if isinstance(type_, GraphQLScalarType):
        return (
            generate_annotation_name(SIMPLE_TYPE_MAP.get(type_.name, ANY), nullable),
            [],
        )

    if isinstance(
        type_,
        (
            GraphQLObjectType,
            GraphQLInterfaceType,
        ),
    ):
        name = class_name + type_.name if add_type_name else class_name
        return (
            generate_annotation_name('"' + name + '"', nullable),
            [FieldNames(name, type_.name)],
        )

    if isinstance(type_, GraphQLEnumType):
        return (
            generate_annotation_name(type_.name, nullable),
            [FieldNames(type_.name, type_.name)],
        )

    if isinstance(type_, GraphQLUnionType):
        annotations = []
        names = []
        for subtype in type_.types:
            sub_annotation, sub_names = parse_operation_field_type(
                subtype, nullable=False, class_name=class_name, add_type_name=True
            )
            annotations.append(sub_annotation)
            names.extend(sub_names)

        return generate_union_annotation(annotations, nullable), names

    if isinstance(type_, GraphQLList):
        slice_, names = parse_operation_field_type(
            cast(CodegenResultFieldType, type_.of_type),
            nullable=nullable,
            class_name=class_name,
        )
        return (generate_list_annotation(slice_=slice_, nullable=nullable), names)

    if isinstance(type_, GraphQLNonNull):
        return parse_operation_field_type(
            type_.of_type, nullable=False, class_name=class_name
        )

    raise ParsingError("Invalid field type.")


def is_nullable(annotation: Annotation) -> bool:
    return (
        isinstance(annotation, ast.Subscript)
        and isinstance(annotation.value, ast.Name)
        and annotation.value.id == OPTIONAL
    )
