import ast

from graphql import GraphQLNamedType

from ariadne_codegen.graphql_schema_generators.utils import (
    get_list_of_named_types,
    get_named_type,
    get_optional_named_type,
)

from ..utils import compare_ast


def test_get_named_type_returns_type_map_call_with_type_cast():
    expected_ast = ast.Call(
        func=ast.Name(id="cast"),
        args=[
            ast.Name(id="GraphQLNamedType"),
            ast.Subscript(
                value=ast.Name(id="type_map"), slice=ast.Constant(value="TestType")
            ),
        ],
        keywords=[],
    )

    assert compare_ast(
        get_named_type(GraphQLNamedType(name="TestType"), "type_map"), expected_ast
    )


def test_get_optional_named_type_for_none_returns_constant_with_none():
    assert compare_ast(get_optional_named_type(None, "type_map"), ast.Constant(None))


def test_get_optional_named_type_for_returns_type_map_call_with_type_cast():
    expected_ast = ast.Call(
        func=ast.Name(id="cast"),
        args=[
            ast.Name(id="GraphQLNamedType"),
            ast.Subscript(
                value=ast.Name(id="type_map"), slice=ast.Constant(value="TestType")
            ),
        ],
        keywords=[],
    )

    assert compare_ast(
        get_optional_named_type(GraphQLNamedType(name="TestType"), "type_map"),
        expected_ast,
    )


def test_get_list_of_named_types_for_empty_list_returns_constant_with_empty_list():
    assert compare_ast(
        get_list_of_named_types([], "type_name", "str"), ast.Constant([])
    )
