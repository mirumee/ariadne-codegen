import ast
from typing import cast

import pytest
from graphql import (
    BooleanValueNode,
    EnumValueNode,
    FloatValueNode,
    GraphQLEnumType,
    GraphQLEnumValueMap,
    GraphQLInputObjectType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLScalarType,
    IntValueNode,
    ListValueNode,
    NameNode,
    NullValueNode,
    ObjectFieldNode,
    ObjectValueNode,
    StringValueNode,
)

from ariadne_codegen.client_generators.constants import (
    FIELD_CLASS,
    LIST,
    MODEL_VALIDATE_METHOD,
    OPTIONAL,
    UPLOAD_CLASS_NAME,
)
from ariadne_codegen.client_generators.input_fields import (
    parse_input_const_value_node,
    parse_input_field_type,
)
from ariadne_codegen.client_generators.scalars import ScalarData

from ..utils import compare_ast


@pytest.mark.parametrize(
    "type_, expected_annotation",
    [
        (GraphQLNonNull(GraphQLScalarType("String")), ast.Name(id="str")),
        (GraphQLNonNull(GraphQLScalarType("ID")), ast.Name(id="str")),
        (GraphQLNonNull(GraphQLScalarType("Int")), ast.Name(id="int")),
        (GraphQLNonNull(GraphQLScalarType("Boolean")), ast.Name(id="bool")),
        (GraphQLNonNull(GraphQLScalarType("Float")), ast.Name(id="float")),
        (GraphQLNonNull(GraphQLScalarType("Upload")), ast.Name(id=UPLOAD_CLASS_NAME)),
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
            GraphQLScalarType("Upload"),
            ast.Subscript(
                value=ast.Name(id=OPTIONAL), slice=ast.Name(id=UPLOAD_CLASS_NAME)
            ),
        ),
        (
            GraphQLScalarType("Other"),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="Any")),
        ),
    ],
)
def test_parse_input_field_type_returns_annotation_for_scalar(
    type_, expected_annotation
):
    annotation, type_name = parse_input_field_type(type_=type_)

    assert compare_ast(annotation, expected_annotation)
    assert type_name == ""


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
            ast.Subscript(value=ast.Name(id=LIST), slice=ast.Name("ScalarXYZ")),
        ),
    ],
)
def test_parse_input_field_type_returns_annotation_for_custom_scalar(
    type_, expected_annotation
):
    annotation, type_name = parse_input_field_type(
        type_=type_, custom_scalars={"SCALARXYZ": ScalarData(type_="ScalarXYZ")}
    )

    assert compare_ast(annotation, expected_annotation)
    assert type_name == "SCALARXYZ"


@pytest.mark.parametrize(
    "type_, expected_annotation, expected_name",
    [
        (
            GraphQLNonNull(GraphQLInputObjectType("TestInput", fields={})),
            ast.Name(id='"TestInput"'),
            "TestInput",
        ),
        (
            GraphQLInputObjectType("TestInput", fields={}),
            ast.Subscript(
                value=ast.Name(id=OPTIONAL), slice=ast.Name(id='"TestInput"')
            ),
            "TestInput",
        ),
    ],
)
def test_parse_input_field_type_returns_annotation_and_type_name_for_input_object_type(
    type_, expected_annotation, expected_name
):
    annotation, type_name = parse_input_field_type(type_=type_)

    assert compare_ast(annotation, expected_annotation)
    assert type_name == expected_name


@pytest.mark.parametrize(
    "type_, expected_annotation, expected_name",
    [
        (
            GraphQLNonNull(
                GraphQLEnumType("TestEnum", values=cast(GraphQLEnumValueMap, {}))
            ),
            ast.Name(id="TestEnum"),
            "TestEnum",
        ),
        (
            GraphQLEnumType("TestEnum", values=cast(GraphQLEnumValueMap, {})),
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="TestEnum")),
            "TestEnum",
        ),
    ],
)
def test_parse_input_field_type_returns_annotation_and_type_name_for_enum_type(
    type_, expected_annotation, expected_name
):
    annotation, type_name = parse_input_field_type(type_=type_)

    assert compare_ast(annotation, expected_annotation)
    assert type_name == expected_name


def test_parse_input_field_type_returns_annotation_for_list():
    type_ = GraphQLNonNull(
        GraphQLList(type_=GraphQLNonNull(GraphQLInputObjectType("TestType", fields={})))
    )
    expected_annotation = ast.Subscript(
        value=ast.Name(id=LIST), slice=ast.Name('"TestType"')
    )
    expected_type_name = "TestType"

    annotation, type_name = parse_input_field_type(type_=type_)

    assert compare_ast(annotation, expected_annotation)
    assert type_name == expected_type_name


@pytest.mark.parametrize(
    "node, field_type, expected_result",
    [
        (IntValueNode(value="10"), "", ast.Constant(value=10)),
        (FloatValueNode(value="9.9"), "", ast.Constant(value=9.9)),
        (StringValueNode(value="test str"), "", ast.Constant(value="test str")),
        (BooleanValueNode(value=True), "", ast.Constant(value=True)),
        (NullValueNode(), "", ast.Constant(value=None)),
        (EnumValueNode(value="VAL"), "TestEnum", ast.Name(id="TestEnum.VAL")),
    ],
)
def test_parse_input_const_value_node_returns_correct_constant(
    node, field_type, expected_result
):
    assert compare_ast(
        parse_input_const_value_node(node=node, field_type=field_type), expected_result
    )


@pytest.mark.parametrize(
    "node, field_type, expected_result",
    [
        (
            ListValueNode(
                values=(StringValueNode(value="a"), StringValueNode(value="b"))
            ),
            "",
            ast.Call(
                func=ast.Name(id=FIELD_CLASS),
                args=[],
                keywords=[
                    ast.keyword(
                        arg="default_factory",
                        value=ast.Lambda(
                            args=ast.arguments(
                                posonlyargs=[],
                                args=[],
                                kwonlyargs=[],
                                kw_defaults=[],
                                defaults=[],
                            ),
                            body=ast.List(
                                elts=[ast.Constant(value="a"), ast.Constant(value="b")]
                            ),
                        ),
                    )
                ],
            ),
        ),
        (
            ListValueNode(
                values=(
                    ListValueNode(
                        values=(StringValueNode(value="a"), StringValueNode(value="b"))
                    ),
                )
            ),
            "",
            ast.Call(
                func=ast.Name(id=FIELD_CLASS),
                args=[],
                keywords=[
                    ast.keyword(
                        arg="default_factory",
                        value=ast.Lambda(
                            args=ast.arguments(
                                posonlyargs=[],
                                args=[],
                                kwonlyargs=[],
                                kw_defaults=[],
                                defaults=[],
                            ),
                            body=ast.List(
                                elts=[
                                    ast.List(
                                        elts=[
                                            ast.Constant(value="a"),
                                            ast.Constant(value="b"),
                                        ]
                                    )
                                ]
                            ),
                        ),
                    )
                ],
            ),
        ),
    ],
)
def test_parse_input_const_value_node_given_list_returns_correct_method_call(
    node, field_type, expected_result
):
    assert compare_ast(
        parse_input_const_value_node(node=node, field_type=field_type), expected_result
    )


@pytest.mark.parametrize(
    "node, field_type, expected_result",
    [
        (
            ObjectValueNode(
                fields=(
                    ObjectFieldNode(
                        name=NameNode(value="fieldA"), value=StringValueNode(value="a")
                    ),
                    ObjectFieldNode(
                        name=NameNode(value="fieldB"), value=StringValueNode(value="B")
                    ),
                )
            ),
            "TestInput",
            ast.Call(
                func=ast.Name(id="Field"),
                args=[],
                keywords=[
                    ast.keyword(
                        arg="default_factory",
                        value=ast.Lambda(
                            args=ast.arguments(
                                posonlyargs=[],
                                args=[],
                                kwonlyargs=[],
                                kw_defaults=[],
                                defaults=[],
                            ),
                            body=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Subscript(
                                        value=ast.Call(
                                            func=ast.Name(id="globals"),
                                            args=[],
                                            keywords=[],
                                        ),
                                        slice=ast.Constant(value="TestInput"),
                                    ),
                                    attr=MODEL_VALIDATE_METHOD,
                                ),
                                args=[
                                    ast.Dict(
                                        keys=[
                                            ast.Constant(value="fieldA"),
                                            ast.Constant(value="fieldB"),
                                        ],
                                        values=[
                                            ast.Constant(value="a"),
                                            ast.Constant(value="B"),
                                        ],
                                    )
                                ],
                                keywords=[],
                            ),
                        ),
                    )
                ],
            ),
        ),
        (
            ObjectValueNode(
                fields=(
                    ObjectFieldNode(
                        name=NameNode(value="nestedField"),
                        value=ObjectValueNode(
                            fields=(
                                ObjectFieldNode(
                                    name=NameNode(value="fieldA"),
                                    value=StringValueNode(value="a"),
                                ),
                            )
                        ),
                    ),
                )
            ),
            "TestInput",
            ast.Call(
                func=ast.Name(id="Field"),
                args=[],
                keywords=[
                    ast.keyword(
                        arg="default_factory",
                        value=ast.Lambda(
                            args=ast.arguments(
                                posonlyargs=[],
                                args=[],
                                kwonlyargs=[],
                                kw_defaults=[],
                                defaults=[],
                            ),
                            body=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Subscript(
                                        value=ast.Call(
                                            func=ast.Name(id="globals"),
                                            args=[],
                                            keywords=[],
                                        ),
                                        slice=ast.Constant(value="TestInput"),
                                    ),
                                    attr=MODEL_VALIDATE_METHOD,
                                ),
                                args=[
                                    ast.Dict(
                                        keys=[ast.Constant(value="nestedField")],
                                        values=[
                                            ast.Dict(
                                                keys=[ast.Constant(value="fieldA")],
                                                values=[ast.Constant(value="a")],
                                            )
                                        ],
                                    )
                                ],
                                keywords=[],
                            ),
                        ),
                    )
                ],
            ),
        ),
    ],
)
def test_parse_input_const_value_node_given_object_returns_correct_method_call(
    node, field_type, expected_result
):
    assert compare_ast(
        parse_input_const_value_node(node=node, field_type=field_type), expected_result
    )
