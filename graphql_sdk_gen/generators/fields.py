from collections import namedtuple
from typing import Tuple, cast

from graphql import (
    GraphQLEnumType,
    GraphQLInputObjectType,
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
    generate_union_annotation,
)
from .constants import ANY, SIMPLE_TYPE_MAP
from .types import Annotation, CodegenFieldType

FieldNames = namedtuple("FieldNames", ["class_name", "type_name"])


def parse_operation_field_type(
    type_: CodegenFieldType,
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

    if isinstance(
        type_,
        (
            GraphQLInputObjectType,
            GraphQLEnumType,
        ),
    ):
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
            cast(CodegenFieldType, type_.of_type),
            nullable=nullable,
            class_name=class_name,
        )
        return (generate_list_annotation(slice_=slice_, nullable=nullable), names)

    if isinstance(type_, GraphQLNonNull):
        return parse_operation_field_type(
            type_.of_type, nullable=False, class_name=class_name
        )

    raise ParsingError("Invalid field type.")
