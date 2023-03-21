import ast
from collections import namedtuple
from typing import Dict, List, Optional, Tuple, cast

from graphql import (
    DirectiveNode,
    FieldNode,
    GraphQLEnumType,
    GraphQLInterfaceType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLUnionType,
    InlineFragmentNode,
)

from ..codegen import (
    generate_annotation_name,
    generate_list_annotation,
    generate_nullable_annotation,
    generate_union_annotation,
)
from ..exceptions import ParsingError
from .constants import (
    ANY,
    INCLUDE_DIRECTIVE_NAME,
    OPTIONAL,
    SIMPLE_TYPE_MAP,
    SKIP_DIRECTIVE_NAME,
)
from .scalars import ScalarData
from .types import Annotation, CodegenResultFieldType

FieldNames = namedtuple("FieldNames", ["class_name", "type_name"])


def parse_operation_field(
    field: FieldNode,
    type_: CodegenResultFieldType,
    directives: Optional[Tuple[DirectiveNode, ...]] = None,
    class_name: str = "",
    custom_scalars: Optional[Dict[str, ScalarData]] = None,
) -> Tuple[Annotation, List[FieldNames]]:
    annotation, field_types_names = parse_operation_field_type(
        field=field, type_=type_, class_name=class_name, custom_scalars=custom_scalars
    )
    if not (is_nullable(annotation)) and directives:
        nullable_directives = [INCLUDE_DIRECTIVE_NAME, SKIP_DIRECTIVE_NAME]
        directives_names = [d.name.value for d in directives]
        if any(n in nullable_directives for n in directives_names):
            annotation = generate_nullable_annotation(annotation)
    return annotation, field_types_names


# pylint: disable=too-many-return-statements, too-many-branches
def parse_operation_field_type(
    field: FieldNode,
    type_: CodegenResultFieldType,
    nullable: bool = True,
    class_name: str = "",
    add_type_name: bool = False,
    custom_scalars: Optional[Dict[str, ScalarData]] = None,
) -> Tuple[Annotation, List[FieldNames]]:
    """Parse graphql type and return generated annotation."""
    if isinstance(type_, GraphQLScalarType):
        if type_.name in SIMPLE_TYPE_MAP:
            return (generate_annotation_name(SIMPLE_TYPE_MAP[type_.name], nullable), [])
        if custom_scalars and type_.name in custom_scalars:
            return (
                generate_annotation_name(custom_scalars[type_.name].type_, nullable),
                [FieldNames(custom_scalars[type_.name].type_, type_.name)],
            )
        return (generate_annotation_name(ANY, nullable), [])

    if isinstance(type_, GraphQLInterfaceType):
        inline_fragments = []
        if field.selection_set:
            inline_fragments = [
                s
                for s in field.selection_set.selections
                if isinstance(s, InlineFragmentNode)
            ]
        if inline_fragments:
            types = [
                generate_annotation_name('"' + class_name + type_.name + '"', False)
            ]
            names = [FieldNames(class_name + type_.name, type_.name)]
            for fragment in inline_fragments:
                type_name = fragment.type_condition.name.value
                types.append(
                    generate_annotation_name('"' + class_name + type_name + '"', False)
                )
                names.append(FieldNames(class_name + type_name, type_name))
            return generate_union_annotation(types=types, nullable=nullable), names

        name = class_name + type_.name if add_type_name else class_name
        return (
            generate_annotation_name('"' + name + '"', nullable),
            [FieldNames(name, type_.name)],
        )

    if isinstance(type_, GraphQLObjectType):
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
                field=field,
                type_=subtype,
                nullable=False,
                class_name=class_name,
                add_type_name=True,
                custom_scalars=custom_scalars,
            )
            annotations.append(sub_annotation)
            names.extend(sub_names)

        return generate_union_annotation(annotations, nullable), names

    if isinstance(type_, GraphQLList):
        slice_, names = parse_operation_field_type(
            field=field,
            type_=cast(CodegenResultFieldType, type_.of_type),
            nullable=nullable,
            class_name=class_name,
            custom_scalars=custom_scalars,
        )
        return (generate_list_annotation(slice_=slice_, nullable=nullable), names)

    if isinstance(type_, GraphQLNonNull):
        return parse_operation_field_type(
            field=field,
            type_=type_.of_type,
            nullable=False,
            class_name=class_name,
            custom_scalars=custom_scalars,
        )

    raise ParsingError("Invalid field type.")


def is_nullable(annotation: Annotation) -> bool:
    return (
        isinstance(annotation, ast.Subscript)
        and isinstance(annotation.value, ast.Name)
        and annotation.value.id == OPTIONAL
    )
