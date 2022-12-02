import ast

import pytest
from graphql import (
    GraphQLEnumType,
    GraphQLEnumValue,
    GraphQLField,
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLInterfaceType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLUnionType,
)

from graphql_sdk_gen.generators.codegen import parse_field_type
from graphql_sdk_gen.generators.constants import ANY, FIELD_CLASS, LIST, OPTIONAL, UNION


@pytest.mark.parametrize(
    "type_name, expected_repr",
    [
        ("String", "str"),
        ("ID", "str"),
        ("Int", "int"),
        ("Boolean", "bool"),
        ("Float", "float"),
        ("Unknown", ANY),
    ],
)
def test_parse_field_type_given_scalar_type_returns_name_object(
    type_name, expected_repr
):
    type_ = GraphQLScalarType(name=type_name)

    result = parse_field_type(type_, False)

    assert isinstance(result, ast.Name)
    assert result.id == expected_repr


@pytest.mark.parametrize(
    "type_name, expected_repr",
    [
        ("String", "str"),
        ("ID", "str"),
        ("Int", "int"),
        ("Boolean", "bool"),
        ("Float", "float"),
        ("Unknown", ANY),
    ],
)
def test_parse_field_type_given_scalar_type_returns_optional_annotation(
    type_name, expected_repr
):
    type_ = GraphQLScalarType(name=type_name)

    result = parse_field_type(type_, True)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
    assert isinstance(result.slice, ast.Name)
    assert result.slice.id == expected_repr


@pytest.mark.parametrize(
    "type_class",
    [GraphQLObjectType, GraphQLInputObjectType, GraphQLInterfaceType],
)
def test_parse_field_type_given_custom_type_returns_name_object(type_class):
    type_name = "Xyz"
    type_ = type_class(
        name=type_name,
        fields={FIELD_CLASS: GraphQLField(type_=GraphQLScalarType(name="String"))},
    )

    result = parse_field_type(type_, False)

    assert isinstance(result, ast.Name)
    assert result.id == f'"{type_name}"'


@pytest.mark.parametrize(
    "type_class",
    [GraphQLObjectType, GraphQLInputObjectType, GraphQLInterfaceType],
)
def test_parse_field_type_given_custom_type_returns_optional_annotation(type_class):
    type_name = "Xyz"
    type_ = type_class(
        name=type_name,
        fields={FIELD_CLASS: GraphQLField(type_=GraphQLScalarType(name="String"))},
    )

    result = parse_field_type(type_, True)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
    assert isinstance(result.slice, ast.Name)
    assert result.slice.id == f'"{type_name}"'


def test_parse_field_type_given_enum_type_returns_name_object():
    type_name = "Xyz"
    type_ = GraphQLEnumType(name=type_name, values={"X": GraphQLEnumValue(value="X")})

    result = parse_field_type(type_, False)

    assert isinstance(result, ast.Name)
    assert result.id == f'"{type_name}"'


def test_parse_field_type_given_enum_type_returns_optional_annotation():
    type_name = "Xyz"
    type_ = GraphQLEnumType(name=type_name, values={"X": GraphQLEnumValue(value="X")})

    result = parse_field_type(type_, True)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
    assert isinstance(result.slice, ast.Name)
    assert result.slice.id == f'"{type_name}"'


def test_parse_field_type_given_union_type_returns_union_annotation():
    type_ = GraphQLUnionType(
        name="xyz",
        types=[
            GraphQLObjectType(
                name="String",
                fields={
                    FIELD_CLASS: GraphQLField(type_=GraphQLScalarType(name="String"))
                },
            )
        ],
    )

    result = parse_field_type(type_, False)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == UNION
    assert isinstance(result.slice, ast.Tuple)


def test_parse_field_type_given_union_type_returns_optional_union_annotation():
    type_ = GraphQLUnionType(
        name="xyz",
        types=[
            GraphQLObjectType(
                name="String",
                fields={
                    FIELD_CLASS: GraphQLField(type_=GraphQLScalarType(name="String"))
                },
            )
        ],
    )

    result = parse_field_type(type_, True)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
    assert isinstance(result.slice, ast.Subscript)
    assert isinstance(result.slice.value, ast.Name)
    assert result.slice.value.id == UNION
    assert isinstance(result.slice.slice, ast.Tuple)


def test_parse_field_type_given_list_type_returns_list_annotation():
    type_ = GraphQLList(GraphQLScalarType(name="String"))

    result = parse_field_type(type_, False)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == LIST


def test_parse_field_type_given_list_type_returns_optional_list_annotation():
    type_ = GraphQLList(GraphQLScalarType(name="String"))

    result = parse_field_type(type_, True)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
    assert isinstance(result.slice, ast.Subscript)
    assert isinstance(result.slice.value, ast.Name)
    assert result.slice.value.id == LIST


@pytest.mark.parametrize(
    "subtype",
    [
        GraphQLScalarType(name="String"),
        GraphQLObjectType(
            name="Xyz",
            fields={FIELD_CLASS: GraphQLField(type_=GraphQLScalarType(name="String"))},
        ),
        GraphQLInputObjectType(
            name="Xyz",
            fields={
                FIELD_CLASS: GraphQLInputField(type_=GraphQLScalarType(name="String"))
            },
        ),
        GraphQLInterfaceType(
            name="Xyz",
            fields={FIELD_CLASS: GraphQLField(type_=GraphQLScalarType(name="String"))},
        ),
        GraphQLEnumType(name="Xyz", values={"X": GraphQLEnumValue(value="X")}),
    ],
)
def test_parse_field_type_given_non_null_type_returns_not_optional_annotation(
    subtype,
):
    type_ = GraphQLNonNull(subtype)

    result = parse_field_type(type_)

    assert not isinstance(result, ast.Subscript)


def test_parse_field_type_given_non_null_list_type_returns_not_optional_annotation():
    type_ = GraphQLNonNull(GraphQLList(GraphQLScalarType(name="String")))

    result = parse_field_type(type_)

    assert isinstance(result, ast.Subscript)
    assert result.value != OPTIONAL


def test_parse_field_type_given_non_null_union_type_returns_not_optional_annotation():
    type_ = GraphQLNonNull(
        GraphQLUnionType(
            name="xyz",
            types=[
                GraphQLObjectType(
                    name="String",
                    fields={
                        FIELD_CLASS: GraphQLField(
                            type_=GraphQLScalarType(name="String")
                        )
                    },
                )
            ],
        )
    )

    result = parse_field_type(type_)

    assert isinstance(result, ast.Subscript)
    assert result.value != OPTIONAL
