import ast
from collections import namedtuple
from typing import Dict, List, Optional, Tuple, cast

from graphql import (
    DirectiveNode,
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    GraphQLEnumType,
    GraphQLInterfaceType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLUnionType,
    InlineFragmentNode,
    SelectionSetNode,
)

from ..codegen import (
    generate_annotation_name,
    generate_constant,
    generate_list_annotation,
    generate_name,
    generate_nullable_annotation,
    generate_pydantic_field,
    generate_subscript,
    generate_tuple,
    generate_union_annotation,
)
from ..exceptions import ParsingError
from .constants import (
    ANNOTATED,
    ANY,
    DISCRIMINATOR_KEYWORD,
    INCLUDE_DIRECTIVE_NAME,
    LITERAL,
    OPTIONAL,
    SIMPLE_TYPE_MAP,
    SKIP_DIRECTIVE_NAME,
    TYPENAME_ALIAS,
    TYPENAME_FIELD_NAME,
    UNION,
)
from .scalars import ScalarData
from .types import Annotation, AnnotationSlice, CodegenResultFieldType

FieldNames = namedtuple("FieldNames", ["class_name", "type_name"])


def parse_operation_field(
    field: FieldNode,
    type_: CodegenResultFieldType,
    directives: Optional[Tuple[DirectiveNode, ...]] = None,
    class_name: str = "",
    typename_values: Optional[List[str]] = None,
    custom_scalars: Optional[Dict[str, ScalarData]] = None,
    fragments_definitions: Optional[Dict[str, FragmentDefinitionNode]] = None,
) -> Tuple[Annotation, List[FieldNames]]:
    if field.name and field.name.value == TYPENAME_FIELD_NAME and typename_values:
        return generate_typename_annotation(typename_values), []

    annotation, field_types_names = parse_operation_field_type(
        field=field,
        type_=type_,
        class_name=class_name,
        custom_scalars=custom_scalars,
        fragments_definitions=fragments_definitions,
    )
    if isinstance(annotation, ast.Subscript):
        annotation.slice = annotate_nested_unions(
            cast(AnnotationSlice, annotation.slice)
        )

    if not (is_nullable(annotation)) and directives:
        nullable_directives = [INCLUDE_DIRECTIVE_NAME, SKIP_DIRECTIVE_NAME]
        directives_names = [d.name.value for d in directives]
        if any(n in nullable_directives for n in directives_names):
            annotation = generate_nullable_annotation(annotation)
    return annotation, field_types_names


def generate_typename_annotation(typename_values: List[str]) -> ast.Subscript:
    elts: List[ast.expr] = [generate_name(f'"{v}"') for v in sorted(typename_values)]
    slice_ = generate_tuple(elts) if len(elts) > 1 else elts[0]
    return generate_subscript(value=generate_name(LITERAL), slice_=slice_)


# pylint: disable=too-many-return-statements, too-many-branches
def parse_operation_field_type(
    field: FieldNode,
    type_: CodegenResultFieldType,
    nullable: bool = True,
    class_name: str = "",
    add_type_name: bool = False,
    custom_scalars: Optional[Dict[str, ScalarData]] = None,
    fragments_definitions: Optional[Dict[str, FragmentDefinitionNode]] = None,
) -> Tuple[Annotation, List[FieldNames]]:
    """Parse graphql type and return generated annotation."""
    if isinstance(type_, GraphQLScalarType):
        if type_.name in SIMPLE_TYPE_MAP:
            return (generate_annotation_name(SIMPLE_TYPE_MAP[type_.name], nullable), [])
        if custom_scalars and type_.name in custom_scalars:
            return (
                generate_annotation_name(
                    custom_scalars[type_.name].type_name, nullable
                ),
                [FieldNames(custom_scalars[type_.name].type_name, type_.name)],
            )
        return (generate_annotation_name(ANY, nullable), [])

    if isinstance(type_, GraphQLInterfaceType):
        inline_fragments = get_inline_fragments_from_selection_set(
            field.selection_set, fragments_definitions
        )
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
                fragments_definitions=fragments_definitions,
            )
            annotations.append(sub_annotation)
            names.extend(sub_names)

        return generate_union_annotation(annotations, nullable), names

    if isinstance(type_, GraphQLList):
        slice_, names = parse_operation_field_type(
            field=field,
            type_=cast(CodegenResultFieldType, type_.of_type),
            class_name=class_name,
            custom_scalars=custom_scalars,
            fragments_definitions=fragments_definitions,
        )
        return (generate_list_annotation(slice_=slice_, nullable=nullable), names)

    if isinstance(type_, GraphQLNonNull):
        return parse_operation_field_type(
            field=field,
            type_=type_.of_type,
            nullable=False,
            class_name=class_name,
            custom_scalars=custom_scalars,
            fragments_definitions=fragments_definitions,
        )

    raise ParsingError("Invalid field type.")


def get_inline_fragments_from_selection_set(
    selection_set: Optional[SelectionSetNode],
    fragments_definitions: Optional[Dict[str, FragmentDefinitionNode]],
) -> List[InlineFragmentNode]:
    if not selection_set:
        return []

    fragments_definitions = fragments_definitions or {}
    inline_fragments: List[InlineFragmentNode] = []

    for selection in selection_set.selections or []:
        if isinstance(selection, InlineFragmentNode):
            inline_fragments.append(selection)
        elif isinstance(selection, FragmentSpreadNode):
            fragment_def = fragments_definitions[selection.name.value]
            inline_fragments.extend(
                get_inline_fragments_from_selection_set(
                    fragment_def.selection_set, fragments_definitions
                )
            )

    return inline_fragments


def annotate_nested_unions(annotation: AnnotationSlice) -> AnnotationSlice:
    if isinstance(annotation, ast.Tuple):
        return generate_tuple(
            [
                annotate_nested_unions(cast(AnnotationSlice, elt))
                for elt in annotation.elts
            ]
        )

    if isinstance(annotation, ast.Name):
        return annotation

    if isinstance(annotation.value, ast.Name) and annotation.value.id == UNION:
        return generate_subscript(
            value=generate_name(ANNOTATED),
            slice_=generate_tuple(
                [
                    annotation,
                    generate_pydantic_field(
                        {DISCRIMINATOR_KEYWORD: generate_constant(TYPENAME_ALIAS)}
                    ),
                ]
            ),
        )

    annotation.slice = annotate_nested_unions(cast(AnnotationSlice, annotation.slice))
    return annotation


def is_nullable(annotation: Annotation) -> bool:
    return (
        isinstance(annotation, ast.Subscript)
        and isinstance(annotation.value, ast.Name)
        and annotation.value.id == OPTIONAL
    )


def is_union(annotation: ast.expr) -> bool:
    return (
        isinstance(annotation, ast.Subscript)
        and isinstance(annotation.value, ast.Name)
        and annotation.value.id == UNION
    )
