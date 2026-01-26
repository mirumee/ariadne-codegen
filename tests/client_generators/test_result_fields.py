import ast
from typing import cast

import pytest
from graphql import (
    DirectiveNode,
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    GraphQLBoolean,
    GraphQLEnumType,
    GraphQLEnumValueMap,
    GraphQLFloat,
    GraphQLID,
    GraphQLInt,
    GraphQLInterfaceType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLSchema,
    GraphQLString,
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
    Definitions,
    FieldContext,
    RelatedClassData,
    annotate_nested_unions,
    is_nullable,
    is_union,
    parse_enum_type,
    parse_interface_type,
    parse_list_type,
    parse_object_type,
    parse_operation_field,
    parse_operation_field_type,
    parse_scalar_type,
    parse_union_type,
)
from ariadne_codegen.client_generators.scalars import ScalarData

from ..utils import compare_ast


@pytest.mark.parametrize(
    "directive, type_, expected_annotation",
    [
        (
            INCLUDE_DIRECTIVE_NAME,
            GraphQLNonNull(GraphQLString),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")),
        ),
        (
            INCLUDE_DIRECTIVE_NAME,
            GraphQLString,
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")),
        ),
        (
            SKIP_DIRECTIVE_NAME,
            GraphQLNonNull(GraphQLString),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")),
        ),
        (
            SKIP_DIRECTIVE_NAME,
            GraphQLString,
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
        type_=GraphQLNonNull(GraphQLString),
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
        type_=GraphQLNonNull(GraphQLString),
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
    "type_, expected_method_name",
    [
        (GraphQLString, "parse_scalar_type"),
        (GraphQLInterfaceType("TestInterface", fields={}), "parse_interface_type"),
        (GraphQLObjectType("TestType", fields={}), "parse_object_type"),
        (
            GraphQLEnumType("TestEnum", values=cast(GraphQLEnumValueMap, {})),
            "parse_enum_type",
        ),
        (
            GraphQLUnionType(
                "UnionType",
                types=[
                    GraphQLObjectType("TestTypeA", fields={}),
                    GraphQLObjectType("TestTypeB", fields={}),
                ],
            ),
            "parse_union_type",
        ),
        (
            GraphQLList(type_=GraphQLObjectType("TestType", fields={})),
            "parse_list_type",
        ),
    ],
)
def test_parse_operation_field_type_calls_correct_method_for_type(
    mocker, type_, expected_method_name
):
    context = FieldContext(
        definitions=Definitions(
            schema=GraphQLSchema(),
            field_node=FieldNode(),
            custom_scalars={},
            fragments_definitions={},
        )
    )
    mocked_method = mocker.patch(
        f"ariadne_codegen.client_generators.result_fields.{expected_method_name}",
        return_value=ast.Name(id="placeholder"),
    )

    parse_operation_field_type(
        type_=type_,
        nullable=True,
        context=context,
        class_name="",
        add_type_name=False,
    )

    assert mocked_method.called


@pytest.mark.parametrize(
    "type_, nullable, expected_annotation",
    [
        (GraphQLString, False, ast.Name(id="str")),
        (GraphQLID, False, ast.Name(id="str")),
        (GraphQLInt, False, ast.Name(id="int")),
        (GraphQLBoolean, False, ast.Name(id="bool")),
        (GraphQLFloat, False, ast.Name(id="float")),
        (GraphQLScalarType("Other"), False, ast.Name(id="Any")),
        (
            GraphQLString,
            True,
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")),
        ),
        (
            GraphQLID,
            True,
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")),
        ),
        (
            GraphQLInt,
            True,
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="int")),
        ),
        (
            GraphQLBoolean,
            True,
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="bool")),
        ),
        (
            GraphQLFloat,
            True,
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="float")),
        ),
        (
            GraphQLScalarType("Other"),
            True,
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="Any")),
        ),
    ],
)
def test_parse_scalar_type_returns_annotation_for_not_custom_scalar(
    type_, nullable, expected_annotation
):
    context = FieldContext(
        definitions=Definitions(
            schema=GraphQLSchema(),
            field_node=FieldNode(),
            custom_scalars={},
            fragments_definitions={},
        )
    )
    annotation = parse_scalar_type(type_=type_, nullable=nullable, context=context)

    assert compare_ast(annotation, expected_annotation)
    assert not context.custom_scalars


@pytest.mark.parametrize(
    "nullable, expected_annotation",
    [
        (False, ast.Name(id="ScalarXYZ")),
        (
            True,
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="ScalarXYZ")),
        ),
    ],
)
def test_parse_scalar_type_returns_annotation_for_custom_scalar(
    nullable, expected_annotation
):
    context = FieldContext(
        definitions=Definitions(
            schema=GraphQLSchema(),
            field_node=FieldNode(),
            custom_scalars={
                "SCALARXYZ": ScalarData(type_="ScalarXYZ", graphql_name="SCALARXYZ")
            },
            fragments_definitions={},
        )
    )
    annotation = parse_scalar_type(
        type_=GraphQLScalarType("SCALARXYZ"), nullable=nullable, context=context
    )

    assert compare_ast(annotation, expected_annotation)
    assert context.custom_scalars == ["SCALARXYZ"]


# (
#     GraphQLList(type_=GraphQLNonNull(GraphQLScalarType("SCALARXYZ"))),
#     False,
#     ast.Subscript(value=ast.Name(id=LIST), slice=ast.Name(id="ScalarXYZ")),
# ),


@pytest.mark.parametrize(
    "nullable, expected_annotation",
    [
        (False, ast.Name(id='"TestClassName"')),
        (
            True,
            ast.Subscript(
                value=ast.Name(id=OPTIONAL), slice=ast.Name(id='"TestClassName"')
            ),
        ),
    ],
)
def test_parse_interface_type_returns_annotation(nullable, expected_annotation):
    context = FieldContext(
        definitions=Definitions(
            schema=GraphQLSchema(),
            field_node=FieldNode(),
            custom_scalars={},
            fragments_definitions={},
        )
    )
    annotation = parse_interface_type(
        type_=GraphQLInterfaceType("TestInterface", fields={}),
        nullable=nullable,
        context=context,
        class_name="TestClassName",
        add_type_name=False,
    )

    assert compare_ast(annotation, expected_annotation)
    assert context.abstract_type
    assert context.related_classes == [
        RelatedClassData(class_name="TestClassName", type_name="TestInterface")
    ]


def test_parse_interface_type_returns_union_for_interface_with_inline_fragments():
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
    context = FieldContext(
        definitions=Definitions(
            schema=GraphQLSchema(),
            field_node=FieldNode(
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
            custom_scalars={},
            fragments_definitions={},
        )
    )

    annotation = parse_interface_type(
        type_=GraphQLInterfaceType("TestInterface", fields={}),
        nullable=True,
        context=context,
        class_name="TestClassName",
        add_type_name=True,
    )

    assert compare_ast(annotation, expected_annotation)
    assert context.related_classes == [
        RelatedClassData(
            class_name="TestClassNameTestInterface", type_name="TestInterface"
        ),
        RelatedClassData(class_name="TestClassNameTypeA", type_name="TypeA"),
        RelatedClassData(class_name="TestClassNameTypeB", type_name="TypeB"),
    ]


def test_parse_interface_type_returns_union_for_inline_fragments_in_fragment():
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
    context = FieldContext(
        definitions=Definitions(
            schema=GraphQLSchema(),
            field_node=FieldNode(
                selection_set=SelectionSetNode(
                    selections=(
                        FragmentSpreadNode(name=NameNode(value="TestFragment")),
                    )
                )
            ),
            custom_scalars={},
            fragments_definitions={
                "TestFragment": FragmentDefinitionNode(
                    name=NameNode(value="TestFragment"),
                    selection_set=SelectionSetNode(
                        selections=(
                            FieldNode(),
                            InlineFragmentNode(
                                type_condition=NamedTypeNode(
                                    name=NameNode(value="TypeA")
                                )
                            ),
                            InlineFragmentNode(
                                type_condition=NamedTypeNode(
                                    name=NameNode(value="TypeB")
                                )
                            ),
                        )
                    ),
                )
            },
        )
    )

    annotation = parse_interface_type(
        type_=GraphQLInterfaceType("TestInterface", fields={}),
        nullable=True,
        context=context,
        class_name="TestClassName",
        add_type_name=True,
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
    "nullable, expected_annotation",
    [
        (False, ast.Name(id='"TestClassName"')),
        (
            True,
            ast.Subscript(
                value=ast.Name(id=OPTIONAL), slice=ast.Name(id='"TestClassName"')
            ),
        ),
    ],
)
def test_parse_object_type_returns_annotation(nullable, expected_annotation):
    context = FieldContext(
        definitions=Definitions(
            schema=GraphQLSchema(),
            field_node=FieldNode(),
            custom_scalars={},
            fragments_definitions={},
        )
    )
    annotation = parse_object_type(
        type_=GraphQLObjectType("TestType", fields={}),
        nullable=nullable,
        context=context,
        class_name="TestClassName",
        add_type_name=False,
    )

    assert compare_ast(annotation, expected_annotation)
    assert not context.abstract_type
    assert context.related_classes == [
        RelatedClassData(class_name="TestClassName", type_name="TestType")
    ]


@pytest.mark.parametrize(
    "nullable, expected_annotation",
    [
        (False, ast.Name(id="TestEnum")),
        (
            True,
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="TestEnum")),
        ),
    ],
)
def test_parse_operation_field_type_returns_annotation_for_enums(
    nullable, expected_annotation
):
    context = FieldContext(
        definitions=Definitions(
            schema=GraphQLSchema(),
            field_node=FieldNode(),
            custom_scalars={},
            fragments_definitions={},
        )
    )
    annotation = parse_enum_type(
        type_=GraphQLEnumType("TestEnum", values=cast(GraphQLEnumValueMap, {})),
        nullable=nullable,
        context=context,
    )

    assert compare_ast(annotation, expected_annotation)
    assert context.enums == ["TestEnum"]


def test_parse_union_type_returns_annotation():
    type_ = GraphQLUnionType(
        "UnionType",
        types=[
            GraphQLObjectType("TestTypeA", fields={}),
            GraphQLObjectType("TestTypeB", fields={}),
        ],
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
    context = FieldContext(
        definitions=Definitions(
            schema=GraphQLSchema(),
            field_node=FieldNode(),
            custom_scalars={},
            fragments_definitions={},
        )
    )

    annotation = parse_union_type(
        type_=type_,
        nullable=False,
        context=context,
        class_name="TestQueryField",
    )

    assert compare_ast(annotation, expected_annotation)
    assert context.related_classes == [
        RelatedClassData(class_name="TestQueryFieldTestTypeA", type_name="TestTypeA"),
        RelatedClassData(class_name="TestQueryFieldTestTypeB", type_name="TestTypeB"),
    ]


@pytest.mark.parametrize(
    "type_, nullable, expected_annotation",
    [
        (
            GraphQLList(type_=GraphQLNonNull(GraphQLObjectType("TestType", fields={}))),
            False,
            ast.Subscript(value=ast.Name(id=LIST), slice=ast.Name('"TestQueryField"')),
        ),
        (
            GraphQLList(type_=GraphQLObjectType("TestType", fields={})),
            False,
            ast.Subscript(
                value=ast.Name(id=LIST),
                slice=ast.Subscript(
                    value=ast.Name(OPTIONAL), slice=ast.Name('"TestQueryField"')
                ),
            ),
        ),
        (
            GraphQLList(type_=GraphQLNonNull(GraphQLObjectType("TestType", fields={}))),
            True,
            ast.Subscript(
                value=ast.Name(OPTIONAL),
                slice=ast.Subscript(
                    value=ast.Name(id=LIST), slice=ast.Name('"TestQueryField"')
                ),
            ),
        ),
        (
            GraphQLList(type_=GraphQLObjectType("TestType", fields={})),
            True,
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
    type_, nullable, expected_annotation
):
    context = FieldContext(
        definitions=Definitions(
            schema=GraphQLSchema(),
            field_node=FieldNode(),
            custom_scalars={},
            fragments_definitions={},
        )
    )
    annotation = parse_list_type(
        type_=type_,
        nullable=nullable,
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
