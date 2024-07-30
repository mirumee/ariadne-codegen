import ast
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, cast

from graphql import (
    DirectiveNode,
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    GraphQLAbstractType,
    GraphQLEnumType,
    GraphQLInterfaceType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLSchema,
    GraphQLUnionType,
    InlineFragmentNode,
    SelectionSetNode,
    is_abstract_type,
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
from .scalars import ScalarData, generate_result_scalar_annotation
from .types import Annotation, AnnotationSlice, CodegenResultFieldType


@dataclass
class Definitions:
    schema: GraphQLSchema
    field_node: FieldNode
    custom_scalars: Dict[str, ScalarData]
    fragments_definitions: Dict[str, FragmentDefinitionNode]


@dataclass
class RelatedClassData:
    class_name: str
    type_name: str


@dataclass
class FieldContext:
    definitions: Definitions
    enums: List[str] = field(default_factory=list)
    custom_scalars: List[str] = field(default_factory=list)
    related_classes: List[RelatedClassData] = field(default_factory=list)
    abstract_type: bool = False


def parse_operation_field(
    schema: GraphQLSchema,
    field: FieldNode,
    type_: CodegenResultFieldType,
    directives: Optional[Tuple[DirectiveNode, ...]] = None,
    class_name: str = "",
    typename_values: Optional[List[str]] = None,
    custom_scalars: Optional[Dict[str, ScalarData]] = None,
    fragments_definitions: Optional[Dict[str, FragmentDefinitionNode]] = None,
) -> Tuple[Annotation, Optional[ast.Constant], FieldContext]:
    default_value: Optional[ast.Constant] = None
    context = FieldContext(
        definitions=Definitions(
            schema=schema,
            field_node=field,
            custom_scalars=custom_scalars if custom_scalars else {},
            fragments_definitions=(
                fragments_definitions if fragments_definitions else {}
            ),
        )
    )

    if field.name and field.name.value == TYPENAME_FIELD_NAME and typename_values:
        return generate_typename_annotation(typename_values), default_value, context

    annotation = parse_operation_field_type(
        type_=type_,
        context=context,
        nullable=True,
        add_type_name=False,
        class_name=class_name,
    )
    if isinstance(annotation, ast.Subscript):
        annotation.slice = annotate_nested_unions(
            cast(AnnotationSlice, annotation.slice)
        )
    annotation, default_value = parse_directives(
        annotation=annotation, directives=directives if directives else tuple()
    )

    return annotation, default_value, context


def generate_typename_annotation(typename_values: List[str]) -> ast.Subscript:
    elts: List[ast.expr] = [generate_name(f'"{v}"') for v in sorted(typename_values)]
    slice_ = generate_tuple(elts) if len(elts) > 1 else elts[0]
    return generate_subscript(value=generate_name(LITERAL), slice_=slice_)


# pylint: disable=too-many-return-statements, too-many-branches
def parse_operation_field_type(
    type_: CodegenResultFieldType,
    nullable: bool,
    context: FieldContext,
    class_name: str,
    add_type_name: bool,
) -> Annotation:
    """Parse graphql type and return generated annotation."""
    if isinstance(type_, GraphQLScalarType):
        return parse_scalar_type(type_=type_, nullable=nullable, context=context)

    if isinstance(type_, GraphQLInterfaceType):
        return parse_interface_type(
            type_=type_,
            nullable=nullable,
            context=context,
            class_name=class_name,
            add_type_name=add_type_name,
        )

    if isinstance(type_, GraphQLObjectType):
        return parse_object_type(
            type_=type_,
            nullable=nullable,
            context=context,
            class_name=class_name,
            add_type_name=add_type_name,
        )

    if isinstance(type_, GraphQLEnumType):
        return parse_enum_type(type_=type_, nullable=nullable, context=context)

    if isinstance(type_, GraphQLUnionType):
        return parse_union_type(
            type_=type_, nullable=nullable, context=context, class_name=class_name
        )

    if isinstance(type_, GraphQLList):
        return parse_list_type(
            type_=type_, nullable=nullable, context=context, class_name=class_name
        )

    if isinstance(type_, GraphQLNonNull):
        return parse_operation_field_type(
            type_=type_.of_type,
            context=context,
            nullable=False,
            class_name=class_name,
            add_type_name=False,
        )

    raise ParsingError("Invalid field type.")


def parse_scalar_type(
    type_: GraphQLScalarType,
    nullable: bool,
    context: FieldContext,
) -> Annotation:
    if type_.name in SIMPLE_TYPE_MAP:
        return generate_annotation_name(SIMPLE_TYPE_MAP[type_.name], nullable)

    if type_.name in context.definitions.custom_scalars:
        context.custom_scalars.append(type_.name)
        annotation = generate_result_scalar_annotation(
            context.definitions.custom_scalars[type_.name]
        )
        if nullable:
            annotation = generate_nullable_annotation(annotation)
        return annotation

    return generate_annotation_name(ANY, nullable)


def parse_interface_type(
    type_: GraphQLInterfaceType,
    nullable: bool,
    context: FieldContext,
    class_name: str,
    add_type_name: bool,
) -> Annotation:
    inline_fragments = get_inline_fragments_from_selection_set(
        context.definitions.field_node.selection_set,
        context.definitions.fragments_definitions,
    )
    fragments_on_subtypes = get_fragments_on_subtype(
        context.definitions.schema,
        context.definitions.field_node.selection_set,
        context.definitions.fragments_definitions,
        type_.name,
    )
    context.abstract_type = True
    if inline_fragments or fragments_on_subtypes:
        types: List[ast.expr] = [
            generate_annotation_name('"' + class_name + type_.name + '"', False)
        ]
        context.related_classes.append(
            RelatedClassData(class_name=class_name + type_.name, type_name=type_.name)
        )
        fragments_types_names = sorted(
            {
                f.type_condition.name.value
                for f in inline_fragments + fragments_on_subtypes
            }
        )
        for fragment_type_name in fragments_types_names:
            types.append(
                generate_annotation_name(
                    '"' + class_name + fragment_type_name + '"', False
                )
            )
            context.related_classes.append(
                RelatedClassData(
                    class_name=class_name + fragment_type_name,
                    type_name=fragment_type_name,
                )
            )
        return generate_union_annotation(types=types, nullable=nullable)

    name = class_name + type_.name if add_type_name else class_name
    context.related_classes.append(
        RelatedClassData(class_name=name, type_name=type_.name)
    )
    return generate_annotation_name('"' + name + '"', nullable)


def parse_object_type(
    type_: GraphQLObjectType,
    nullable: bool,
    context: FieldContext,
    class_name: str,
    add_type_name: bool,
) -> Annotation:
    name = class_name + type_.name if add_type_name else class_name
    context.related_classes.append(
        RelatedClassData(class_name=name, type_name=type_.name)
    )
    return generate_annotation_name('"' + name + '"', nullable)


def parse_enum_type(
    type_: GraphQLEnumType, nullable: bool, context: FieldContext
) -> Annotation:
    context.enums.append(type_.name)
    return generate_annotation_name(type_.name, nullable)


def parse_union_type(
    type_: GraphQLUnionType,
    nullable: bool,
    context: FieldContext,
    class_name: str,
) -> Annotation:
    context.abstract_type = True
    sub_annotations: List[ast.expr] = [
        parse_operation_field_type(
            type_=subtype,
            context=context,
            nullable=False,
            class_name=class_name,
            add_type_name=True,
        )
        for subtype in type_.types
    ]

    return generate_union_annotation(sub_annotations, nullable)


def parse_list_type(
    type_: GraphQLList,
    nullable: bool,
    context: FieldContext,
    class_name: str,
) -> Annotation:
    slice_ = parse_operation_field_type(
        type_=cast(CodegenResultFieldType, type_.of_type),
        context=context,
        nullable=True,
        class_name=class_name,
        add_type_name=False,
    )
    return generate_list_annotation(slice_=slice_, nullable=nullable)


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


def get_fragments_on_subtype(
    schema: GraphQLSchema,
    selection_set: Optional[SelectionSetNode],
    fragments_definitions: Optional[Dict[str, FragmentDefinitionNode]],
    root_type: str,
) -> List[FragmentDefinitionNode]:
    root_type_def = schema.get_type(root_type)
    if (
        not selection_set
        or root_type_def is None
        or not is_abstract_type(root_type_def)
    ):
        return []

    root_type_def = cast(GraphQLAbstractType, root_type_def)
    fragments_definitions = fragments_definitions or {}
    fragments = []

    for selection in selection_set.selections or []:
        if isinstance(selection, FragmentSpreadNode):
            fragment_def = fragments_definitions[selection.name.value]
            fragment_root_type_def = schema.get_type(
                fragment_def.type_condition.name.value
            )

            if fragment_root_type_def and schema.is_sub_type(
                root_type_def, fragment_root_type_def
            ):
                fragments.append(fragment_def)

    return fragments


def annotate_nested_unions(annotation: AnnotationSlice) -> AnnotationSlice:
    if isinstance(annotation, ast.Tuple):
        return generate_tuple(
            [
                annotate_nested_unions(cast(AnnotationSlice, elt))
                for elt in annotation.elts
            ]
        )

    if isinstance(annotation, (ast.Name, ast.Call)):
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


def parse_directives(
    annotation: Annotation, directives: Tuple[DirectiveNode, ...]
) -> Tuple[Annotation, Optional[ast.Constant]]:
    nullable_directives = (INCLUDE_DIRECTIVE_NAME, SKIP_DIRECTIVE_NAME)
    directives_names = [d.name.value for d in directives]

    if any(n in nullable_directives for n in directives_names):
        if not is_nullable(annotation):
            annotation = generate_nullable_annotation(annotation)
        return annotation, generate_constant(None)

    return annotation, None


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
