import ast
from typing import cast

import pytest
from graphql import (
    DirectiveNode,
    FieldNode,
    GraphQLEnumType,
    GraphQLEnumValueMap,
    GraphQLInterfaceType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLUnionType,
    NameNode,
)

from ariadne_codegen.generators.constants import (
    INCLUDE_DIRECTIVE_NAME,
    LIST,
    OPTIONAL,
    SKIP_DIRECTIVE_NAME,
    UNION,
)
from ariadne_codegen.generators.result_fields import (
    FieldNames,
    is_nullable,
    parse_operation_field,
    parse_operation_field_type,
)
from ariadne_codegen.generators.scalars import ScalarData

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
    annotation, _ = parse_operation_field(
        field=FieldNode(),
        type_=type_,
        directives=(DirectiveNode(name=NameNode(value=directive), arguments=()),),
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
    annotation, names = parse_operation_field_type(field=FieldNode(), type_=type_)

    assert compare_ast(annotation, expected_annotation)
    assert names == []


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
    annotation, names = parse_operation_field_type(
        field=FieldNode(),
        type_=type_,
        custom_scalars={"SCALARXYZ": ScalarData(type_="ScalarXYZ")},
    )

    assert compare_ast(annotation, expected_annotation)
    assert names == [FieldNames(class_name="ScalarXYZ", type_name="SCALARXYZ")]


@pytest.mark.parametrize(
    "type_, class_name, expected_annotation, expected_names",
    [
        (
            GraphQLNonNull(GraphQLObjectType("TestType", fields={})),
            "TestClassName",
            ast.Name(id='"TestClassName"'),
            [FieldNames(class_name="TestClassName", type_name="TestType")],
        ),
        (
            GraphQLObjectType("TestType", fields={}),
            "TestClassName",
            ast.Subscript(
                value=ast.Name(id=OPTIONAL), slice=ast.Name(id='"TestClassName"')
            ),
            [FieldNames(class_name="TestClassName", type_name="TestType")],
        ),
        (
            GraphQLNonNull(GraphQLInterfaceType("TestInterface", fields={})),
            "TestClassName",
            ast.Name(id='"TestClassName"'),
            [FieldNames(class_name="TestClassName", type_name="TestInterface")],
        ),
        (
            GraphQLInterfaceType("TestInterface", fields={}),
            "TestClassName",
            ast.Subscript(
                value=ast.Name(id=OPTIONAL), slice=ast.Name(id='"TestClassName"')
            ),
            [FieldNames(class_name="TestClassName", type_name="TestInterface")],
        ),
    ],
)
def test_parse_operation_field_type_returns_annotation_for_objects_and_interfaces(
    type_, class_name, expected_annotation, expected_names
):
    annotation, names = parse_operation_field_type(
        field=FieldNode(), type_=type_, class_name=class_name
    )

    assert compare_ast(annotation, expected_annotation)
    assert names == expected_names


@pytest.mark.parametrize(
    "type_, expected_annotation, expected_names",
    [
        (
            GraphQLNonNull(
                GraphQLEnumType("TestEnum", values=cast(GraphQLEnumValueMap, {}))
            ),
            ast.Name(id="TestEnum"),
            [FieldNames(class_name="TestEnum", type_name="TestEnum")],
        ),
        (
            GraphQLEnumType("TestEnum", values=cast(GraphQLEnumValueMap, {})),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="TestEnum")),
            [FieldNames(class_name="TestEnum", type_name="TestEnum")],
        ),
    ],
)
def test_parse_operation_field_type_returns_annotation_for_enums(
    type_, expected_annotation, expected_names
):
    annotation, names = parse_operation_field_type(field=FieldNode(), type_=type_)

    assert compare_ast(annotation, expected_annotation)
    assert names == expected_names


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
    expected_names = [
        FieldNames(class_name="TestQueryFieldTestTypeA", type_name="TestTypeA"),
        FieldNames(class_name="TestQueryFieldTestTypeB", type_name="TestTypeB"),
    ]

    annotation, names = parse_operation_field_type(
        field=FieldNode(), type_=type_, class_name="TestQueryField"
    )

    assert compare_ast(annotation, expected_annotation)
    assert names == expected_names


def test_parse_operation_field_type_returns_annotation_for_list():
    type_ = GraphQLNonNull(
        GraphQLList(type_=GraphQLNonNull(GraphQLObjectType("TestType", fields={})))
    )
    expected_annotation = ast.Subscript(
        value=ast.Name(id=LIST), slice=ast.Name('"TestQueryField"')
    )

    expected_names = [
        FieldNames(class_name="TestQueryField", type_name="TestType"),
    ]

    annotation, names = parse_operation_field_type(
        field=FieldNode(), type_=type_, class_name="TestQueryField"
    )

    assert compare_ast(annotation, expected_annotation)
    assert names == expected_names


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
