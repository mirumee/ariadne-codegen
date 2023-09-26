import ast
from typing import cast

import pytest
from graphql import (
    DirectiveNode,
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    GraphQLEnumType,
    GraphQLEnumValueMap,
    GraphQLInterfaceType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLSchema,
    GraphQLUnionType,
    InlineFragmentNode,
    NamedTypeNode,
    NameNode,
    SelectionSetNode,
)

from ariadne_codegen.client_generators.constants import (
    ANNOTATED,
    DISCRIMINATOR_KEYWORD,
    FIELD_CLASS,
    INCLUDE_DIRECTIVE_NAME,
    LIST,
    LITERAL,
    OPTIONAL,
    SKIP_DIRECTIVE_NAME,
    TYPENAME_ALIAS,
    TYPENAME_FIELD_NAME,
    UNION,
)
from ariadne_codegen.client_generators.result_fields import (
    FieldContext,
    RelatedClassData,
    annotate_nested_unions,
    is_nullable,
    is_union,
    parse_operation_field,
    parse_operation_field_type,
)
from ariadne_codegen.client_generators.scalars import ScalarData

from ..utils import compare_ast


@pytest.mark.parametrize(
    "directive, type_, expected_annotation",
    [
        (
            INCLUDE_DIRECTIVE_NAME,
            GraphQLNonNull(GraphQLScalarType("String")),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")),
        ),
        (
            INCLUDE_DIRECTIVE_NAME,
            GraphQLScalarType("String"),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")),
        ),
        (
            SKIP_DIRECTIVE_NAME,
            GraphQLNonNull(GraphQLScalarType("String")),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")),
        ),
        (
            SKIP_DIRECTIVE_NAME,
            GraphQLScalarType("String"),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")),
        ),
    ],
)
def test_parse_operation_field_returns_optional_annotation_if_given_nullable_directive(
    directive, type_, expected_annotation
):
    annotation, _, _ = parse_operation_field(
        schema=GraphQLSchema(),
        field=FieldNode(),
        type_=type_,
        directives=(DirectiveNode(name=NameNode(value=directive), arguments=()),),
    )

    assert compare_ast(annotation, expected_annotation)


def test_parse_operation_field_returns_typename_annotation_with_multiple_values():
    expected_annotation = ast.Subscript(
        value=ast.Name(id=LITERAL),
        slice=ast.Tuple(elts=[ast.Name(id='"TypeA"'), ast.Name(id='"TypeB"')]),
    )

    annotation, _, _ = parse_operation_field(
        schema=GraphQLSchema(),
        field=FieldNode(name=NameNode(value=TYPENAME_FIELD_NAME)),
        type_=GraphQLNonNull(GraphQLScalarType("String")),
        typename_values=["TypeB", "TypeA"],
    )

    assert compare_ast(annotation, expected_annotation)


def test_parse_operation_field_returns_typename_annotation_with_single_value():
    expected_annotation = ast.Subscript(
        value=ast.Name(id=LITERAL), slice=ast.Name(id='"TypeA"')
    )

    annotation, _, _ = parse_operation_field(
        schema=GraphQLSchema(),
        field=FieldNode(name=NameNode(value=TYPENAME_FIELD_NAME)),
        type_=GraphQLNonNull(GraphQLScalarType("String")),
        typename_values=["TypeA"],
    )

    assert compare_ast(annotation, expected_annotation)


def test_parse_operation_field_returns_annotation_with_annotated_nested_unions():
    expected_annotation = ast.Subscript(
        value=ast.Name(id=OPTIONAL),
        slice=ast.Subscript(
            value=ast.Name(id=ANNOTATED),
            slice=ast.Tuple(
                elts=[
                    ast.Subscript(
                        value=ast.Name(id=UNION),
                        slice=ast.Tuple(
                            elts=[ast.Name(id='"TypeA"'), ast.Name(id='"TypeB"')]
                        ),
                    ),
                    ast.Call(
                        func=ast.Name(id=FIELD_CLASS),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg=DISCRIMINATOR_KEYWORD,
                                value=ast.Constant(value=TYPENAME_ALIAS),
                            )
                        ],
                    ),
                ]
            ),
        ),
    )

    annotation, _, _ = parse_operation_field(
        schema=GraphQLSchema(),
        field=FieldNode(name=NameNode(value="unionField")),
        type_=GraphQLUnionType(
            "UnionType",
            types=[
                GraphQLObjectType("TypeA", fields={}),
                GraphQLObjectType("TypeB", fields={}),
            ],
        ),
        typename_values=["TypeA", "TypeB"],
    )

    assert compare_ast(annotation, expected_annotation)


@pytest.mark.parametrize(
    "type_, expected_annotation",
    [
        (GraphQLNonNull(GraphQLScalarType("String")), ast.Name(id="str")),
        (GraphQLNonNull(GraphQLScalarType("ID")), ast.Name(id="str")),
        (GraphQLNonNull(GraphQLScalarType("Int")), ast.Name(id="int")),
        (GraphQLNonNull(GraphQLScalarType("Boolean")), ast.Name(id="bool")),
        (GraphQLNonNull(GraphQLScalarType("Float")), ast.Name(id="float")),
        (GraphQLNonNull(GraphQLScalarType("Other")), ast.Name(id="Any")),
        (
            GraphQLScalarType("String"),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")),
        ),
        (
            GraphQLScalarType("ID"),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")),
        ),
        (
            GraphQLScalarType("Int"),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="int")),
        ),
        (
            GraphQLScalarType("Boolean"),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="bool")),
        ),
        (
            GraphQLScalarType("Float"),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="float")),
        ),
        (
            GraphQLScalarType("Other"),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="Any")),
        ),
    ],
)
def test_parse_operation_field_type_returns_annotation_for_scalar(
    type_, expected_annotation
):
    context = FieldContext()
    annotation = parse_operation_field_type(
        schema=GraphQLSchema(), field=FieldNode(), type_=type_, context=context
    )

    assert compare_ast(annotation, expected_annotation)
    assert not context.custom_scalars


@pytest.mark.parametrize(
    "type_, expected_annotation",
    [
        (GraphQLNonNull(GraphQLScalarType("SCALARXYZ")), ast.Name(id="ScalarXYZ")),
        (
            GraphQLScalarType("SCALARXYZ"),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="ScalarXYZ")),
        ),
        (
            GraphQLNonNull(
                GraphQLList(type_=GraphQLNonNull(GraphQLScalarType("SCALARXYZ")))
            ),
            ast.Subscript(value=ast.Name(id=LIST), slice=ast.Name(id="ScalarXYZ")),
        ),
    ],
)
def test_parse_operation_field_type_returns_annotation_for_custom_scalar(
    type_, expected_annotation
):
    context = FieldContext()
    annotation = parse_operation_field_type(
        schema=GraphQLSchema(),
        field=FieldNode(),
        type_=type_,
        context=context,
        custom_scalars={
            "SCALARXYZ": ScalarData(type_="ScalarXYZ", graphql_name="SCALARXYZ")
        },
    )

    assert compare_ast(annotation, expected_annotation)
    assert context.custom_scalars == ["SCALARXYZ"]


@pytest.mark.parametrize(
    "type_, class_name, expected_annotation, expected_related_classes",
    [
        (
            GraphQLNonNull(GraphQLObjectType("TestType", fields={})),
            "TestClassName",
            ast.Name(id='"TestClassName"'),
            [RelatedClassData(class_name="TestClassName", type_name="TestType")],
        ),
        (
            GraphQLObjectType("TestType", fields={}),
            "TestClassName",
            ast.Subscript(
                value=ast.Name(id=OPTIONAL), slice=ast.Name(id='"TestClassName"')
            ),
            [RelatedClassData(class_name="TestClassName", type_name="TestType")],
        ),
    ],
)
def test_parse_operation_field_type_returns_annotation_for_object(
    type_, class_name, expected_annotation, expected_related_classes
):
    context = FieldContext()
    annotation = parse_operation_field_type(
        schema=GraphQLSchema(),
        field=FieldNode(),
        type_=type_,
        context=context,
        class_name=class_name,
    )

    assert compare_ast(annotation, expected_annotation)
    assert not context.abstract_type
    assert context.related_classes == expected_related_classes


@pytest.mark.parametrize(
    "type_, class_name, expected_annotation, expected_related_classes",
    [
        (
            GraphQLNonNull(GraphQLInterfaceType("TestInterface", fields={})),
            "TestClassName",
            ast.Name(id='"TestClassName"'),
            [RelatedClassData(class_name="TestClassName", type_name="TestInterface")],
        ),
        (
            GraphQLInterfaceType("TestInterface", fields={}),
            "TestClassName",
            ast.Subscript(
                value=ast.Name(id=OPTIONAL), slice=ast.Name(id='"TestClassName"')
            ),
            [RelatedClassData(class_name="TestClassName", type_name="TestInterface")],
        ),
    ],
)
def test_parse_operation_field_type_returns_annotation_interface(
    type_, class_name, expected_annotation, expected_related_classes
):
    context = FieldContext()
    annotation = parse_operation_field_type(
        schema=GraphQLSchema(),
        field=FieldNode(),
        type_=type_,
        context=context,
        class_name=class_name,
    )

    assert compare_ast(annotation, expected_annotation)
    assert context.abstract_type
    assert context.related_classes == expected_related_classes


def test_parse_operation_field_type_returns_union_for_interface_with_inline_fragments():
    expected_annotation = ast.Subscript(
        value=ast.Name(id=OPTIONAL),
        slice=ast.Subscript(
            value=ast.Name(id=UNION),
            slice=ast.Tuple(
                elts=[
                    ast.Name(id='"TestClassNameTestInterface"'),
                    ast.Name(id='"TestClassNameTypeA"'),
                    ast.Name(id='"TestClassNameTypeB"'),
                ]
            ),
        ),
    )
    context = FieldContext()

    annotation = parse_operation_field_type(
        schema=GraphQLSchema(),
        field=FieldNode(
            selection_set=SelectionSetNode(
                selections=(
                    FieldNode(),
                    InlineFragmentNode(
                        type_condition=NamedTypeNode(name=NameNode(value="TypeA"))
                    ),
                    InlineFragmentNode(
                        type_condition=NamedTypeNode(name=NameNode(value="TypeB"))
                    ),
                )
            )
        ),
        type_=GraphQLInterfaceType("TestInterface", fields={}),
        context=context,
        class_name="TestClassName",
    )

    assert compare_ast(annotation, expected_annotation)
    assert context.related_classes == [
        RelatedClassData(
            class_name="TestClassNameTestInterface", type_name="TestInterface"
        ),
        RelatedClassData(class_name="TestClassNameTypeA", type_name="TypeA"),
        RelatedClassData(class_name="TestClassNameTypeB", type_name="TypeB"),
    ]


def test_parse_operation_field_type_returns_union_inline_fragments_in_fragment():
    expected_annotation = ast.Subscript(
        value=ast.Name(id=OPTIONAL),
        slice=ast.Subscript(
            value=ast.Name(id=UNION),
            slice=ast.Tuple(
                elts=[
                    ast.Name(id='"TestClassNameTestInterface"'),
                    ast.Name(id='"TestClassNameTypeA"'),
                    ast.Name(id='"TestClassNameTypeB"'),
                ]
            ),
        ),
    )
    fragment_def = FragmentDefinitionNode(
        name=NameNode(value="TestFragment"),
        selection_set=SelectionSetNode(
            selections=(
                FieldNode(),
                InlineFragmentNode(
                    type_condition=NamedTypeNode(name=NameNode(value="TypeA"))
                ),
                InlineFragmentNode(
                    type_condition=NamedTypeNode(name=NameNode(value="TypeB"))
                ),
            )
        ),
    )
    context = FieldContext()

    annotation = parse_operation_field_type(
        schema=GraphQLSchema(),
        field=FieldNode(
            selection_set=SelectionSetNode(
                selections=(FragmentSpreadNode(name=NameNode(value="TestFragment")),)
            )
        ),
        type_=GraphQLInterfaceType("TestInterface", fields={}),
        context=context,
        class_name="TestClassName",
        fragments_definitions={"TestFragment": fragment_def},
    )

    assert compare_ast(annotation, expected_annotation)
    assert context.related_classes == [
        RelatedClassData(
            class_name="TestClassNameTestInterface", type_name="TestInterface"
        ),
        RelatedClassData(class_name="TestClassNameTypeA", type_name="TypeA"),
        RelatedClassData(class_name="TestClassNameTypeB", type_name="TypeB"),
    ]


@pytest.mark.parametrize(
    "type_, expected_annotation",
    [
        (
            GraphQLNonNull(
                GraphQLEnumType("TestEnum", values=cast(GraphQLEnumValueMap, {}))
            ),
            ast.Name(id="TestEnum"),
        ),
        (
            GraphQLEnumType("TestEnum", values=cast(GraphQLEnumValueMap, {})),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="TestEnum")),
        ),
    ],
)
def test_parse_operation_field_type_returns_annotation_for_enums(
    type_, expected_annotation
):
    context = FieldContext()
    annotation = parse_operation_field_type(
        schema=GraphQLSchema(), field=FieldNode(), type_=type_, context=context
    )

    assert compare_ast(annotation, expected_annotation)
    assert context.enums == ["TestEnum"]


def test_parse_operation_field_type_returns_annotation_and_names_for_union():
    type_ = GraphQLNonNull(
        GraphQLUnionType(
            "UnionType",
            types=[
                GraphQLObjectType("TestTypeA", fields={}),
                GraphQLObjectType("TestTypeB", fields={}),
            ],
        )
    )
    expected_annotation = ast.Subscript(
        value=ast.Name(id=UNION),
        slice=ast.Tuple(
            elts=[
                ast.Name('"TestQueryFieldTestTypeA"'),
                ast.Name('"TestQueryFieldTestTypeB"'),
            ]
        ),
    )
    context = FieldContext()

    annotation = parse_operation_field_type(
        schema=GraphQLSchema(),
        field=FieldNode(),
        type_=type_,
        context=context,
        class_name="TestQueryField",
    )

    assert compare_ast(annotation, expected_annotation)
    assert context.related_classes == [
        RelatedClassData(class_name="TestQueryFieldTestTypeA", type_name="TestTypeA"),
        RelatedClassData(class_name="TestQueryFieldTestTypeB", type_name="TestTypeB"),
    ]


@pytest.mark.parametrize(
    "type_, expected_annotation",
    [
        (
            GraphQLNonNull(
                GraphQLList(
                    type_=GraphQLNonNull(GraphQLObjectType("TestType", fields={}))
                )
            ),
            ast.Subscript(value=ast.Name(id=LIST), slice=ast.Name('"TestQueryField"')),
        ),
        (
            GraphQLNonNull(GraphQLList(type_=GraphQLObjectType("TestType", fields={}))),
            ast.Subscript(
                value=ast.Name(id=LIST),
                slice=ast.Subscript(
                    value=ast.Name(OPTIONAL), slice=ast.Name('"TestQueryField"')
                ),
            ),
        ),
        (
            GraphQLList(type_=GraphQLNonNull(GraphQLObjectType("TestType", fields={}))),
            ast.Subscript(
                value=ast.Name(OPTIONAL),
                slice=ast.Subscript(
                    value=ast.Name(id=LIST), slice=ast.Name('"TestQueryField"')
                ),
            ),
        ),
        (
            GraphQLList(type_=GraphQLObjectType("TestType", fields={})),
            ast.Subscript(
                value=ast.Name(OPTIONAL),
                slice=ast.Subscript(
                    value=ast.Name(id=LIST),
                    slice=ast.Subscript(
                        value=ast.Name(OPTIONAL), slice=ast.Name('"TestQueryField"')
                    ),
                ),
            ),
        ),
    ],
)
def test_parse_operation_field_type_returns_annotation_for_list(
    type_, expected_annotation
):
    context = FieldContext()
    annotation = parse_operation_field_type(
        schema=GraphQLSchema(),
        field=FieldNode(),
        type_=type_,
        context=context,
        class_name="TestQueryField",
    )

    assert compare_ast(annotation, expected_annotation)
    assert context.related_classes == [
        RelatedClassData(class_name="TestQueryField", type_name="TestType"),
    ]


@pytest.mark.parametrize(
    "annotation, expected",
    [
        (
            ast.Subscript(
                value=ast.Name(id=UNION),
                slice=ast.Tuple(elts=[ast.Name(id='"TypeA"'), ast.Name(id='"TypeB"')]),
            ),
            ast.Subscript(
                value=ast.Name(id=ANNOTATED),
                slice=ast.Tuple(
                    elts=[
                        ast.Subscript(
                            value=ast.Name(id=UNION),
                            slice=ast.Tuple(
                                elts=[ast.Name(id='"TypeA"'), ast.Name(id='"TypeB"')]
                            ),
                        ),
                        ast.Call(
                            func=ast.Name(id=FIELD_CLASS),
                            args=[],
                            keywords=[
                                ast.keyword(
                                    arg=DISCRIMINATOR_KEYWORD,
                                    value=ast.Constant(value=TYPENAME_ALIAS),
                                )
                            ],
                        ),
                    ]
                ),
            ),
        ),
        (
            ast.Subscript(
                value=ast.Name(id=LIST),
                slice=ast.Subscript(
                    value=ast.Name(id=UNION),
                    slice=ast.Tuple(
                        elts=[ast.Name(id='"TypeA"'), ast.Name(id='"TypeB"')]
                    ),
                ),
            ),
            ast.Subscript(
                value=ast.Name(id=LIST),
                slice=ast.Subscript(
                    value=ast.Name(id=ANNOTATED),
                    slice=ast.Tuple(
                        elts=[
                            ast.Subscript(
                                value=ast.Name(id=UNION),
                                slice=ast.Tuple(
                                    elts=[
                                        ast.Name(id='"TypeA"'),
                                        ast.Name(id='"TypeB"'),
                                    ]
                                ),
                            ),
                            ast.Call(
                                func=ast.Name(id=FIELD_CLASS),
                                args=[],
                                keywords=[
                                    ast.keyword(
                                        arg=DISCRIMINATOR_KEYWORD,
                                        value=ast.Constant(value=TYPENAME_ALIAS),
                                    )
                                ],
                            ),
                        ]
                    ),
                ),
            ),
        ),
    ],
)
def test_annotate_nested_unions_returns_annotated_union(annotation, expected):
    assert compare_ast(annotate_nested_unions(annotation), expected)


@pytest.mark.parametrize(
    "annotation",
    [
        ast.Name(id="TestName"),
        ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="TestName")),
        ast.Subscript(value=ast.Name(id=LIST), slice=ast.Name(id="TestName")),
    ],
)
def test_annotate_nested_unions_doesnt_change_not_unions(annotation):
    assert compare_ast(annotate_nested_unions(annotation), annotation)


@pytest.mark.parametrize(
    "annotation, expected",
    [
        (ast.Name(id="TestName"), False),
        (
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="TestName")),
            True,
        ),
        (
            ast.Subscript(value=ast.Name(id=UNION), slice=ast.Name(id="TestName")),
            False,
        ),
    ],
)
def test_is_nullable(annotation, expected):
    assert is_nullable(annotation) == expected


@pytest.mark.parametrize(
    "annotation, expected",
    [
        (ast.Name(id="TypeA"), False),
        (
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="TypeA")),
            False,
        ),
        (
            ast.Subscript(value=ast.Name(id=UNION), slice=ast.Name(id="TypeA")),
            True,
        ),
        (
            ast.Subscript(
                value=ast.Name(id=OPTIONAL),
                slice=ast.Subscript(
                    value=ast.Name(id=UNION), slice=ast.Name(id="TypeA")
                ),
            ),
            False,
        ),
    ],
)
def test_is_union(annotation, expected):
    assert is_union(annotation) is expected
