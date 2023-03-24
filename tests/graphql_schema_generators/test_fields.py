import ast

import pytest
from graphql import (
    GraphQLArgument,
    GraphQLBoolean,
    GraphQLEnumType,
    GraphQLEnumValue,
    GraphQLField,
    GraphQLFloat,
    GraphQLID,
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLInt,
    GraphQLInterfaceType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLString,
    GraphQLUnionType,
    Undefined,
)

from ariadne_codegen.graphql_schema_generators.fields import (
    generate_arg,
    generate_args,
    generate_enum_value,
    generate_enum_values,
    generate_field,
    generate_field_map,
    generate_field_type,
    generate_input_field,
    generate_input_field_map,
)

from ..utils import compare_ast


def test_generate_field_map_returns_correct_lambda():
    field_map = {
        "field1": GraphQLField(
            GraphQLObjectType(name="TestType", fields={}),
            args={
                "arg1": GraphQLArgument(
                    type_=GraphQLString,
                    default_value="default_value",
                    description="arg1_description",
                )
            },
            description="description",
            deprecation_reason="reason",
        ),
        "field2": GraphQLField(GraphQLString),
    }
    expected_ast = ast.Lambda(
        args=ast.arguments(
            posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]
        ),
        body=ast.Dict(
            keys=[ast.Constant(value="field1"), ast.Constant(value="field2")],
            values=[
                ast.Call(
                    func=ast.Name(id="GraphQLField"),
                    args=[
                        ast.Call(
                            func=ast.Name(id="cast"),
                            args=[
                                ast.Name(id="GraphQLObjectType"),
                                ast.Subscript(
                                    value=ast.Name(id="type_map"),
                                    slice=ast.Constant(value="TestType"),
                                ),
                            ],
                            keywords=[],
                        )
                    ],
                    keywords=[
                        ast.keyword(
                            arg="args",
                            value=ast.Dict(
                                keys=[ast.Constant(value="arg1")],
                                values=[
                                    ast.Call(
                                        func=ast.Name(id="GraphQLArgument"),
                                        args=[ast.Name(id="GraphQLString")],
                                        keywords=[
                                            ast.keyword(
                                                arg="default_value",
                                                value=ast.Constant(
                                                    value="default_value"
                                                ),
                                            ),
                                            ast.keyword(
                                                arg="description",
                                                value=ast.Constant(
                                                    value="arg1_description"
                                                ),
                                            ),
                                            ast.keyword(
                                                arg="deprecation_reason",
                                                value=ast.Constant(value=None),
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        ),
                        ast.keyword(
                            arg="description", value=ast.Constant(value="description")
                        ),
                        ast.keyword(
                            arg="deprecation_reason", value=ast.Constant(value="reason")
                        ),
                    ],
                ),
                ast.Call(
                    func=ast.Name(id="GraphQLField"),
                    args=[ast.Name(id="GraphQLString")],
                    keywords=[
                        ast.keyword(arg="args", value=ast.Dict(keys=[], values=[])),
                        ast.keyword(arg="description", value=ast.Constant(value=None)),
                        ast.keyword(
                            arg="deprecation_reason", value=ast.Constant(value=None)
                        ),
                    ],
                ),
            ],
        ),
    )

    a = generate_field_map(field_map, "type_map")

    assert compare_ast(generate_field_map(field_map, "type_map"), expected_ast)


def test_generate_field_returns_correct_ast_call():
    field = GraphQLField(
        GraphQLObjectType(name="TestType", fields={}),
        args={
            "arg1": GraphQLArgument(
                type_=GraphQLString,
                default_value="default_value",
                description="arg1_description",
            )
        },
        description="description",
        deprecation_reason="reason",
    )
    expected_ast = ast.Call(
        func=ast.Name(id="GraphQLField"),
        args=[
            ast.Call(
                func=ast.Name(id="cast"),
                args=[
                    ast.Name(id="GraphQLObjectType"),
                    ast.Subscript(
                        value=ast.Name(id="type_map"),
                        slice=ast.Constant(value="TestType"),
                    ),
                ],
                keywords=[],
            )
        ],
        keywords=[
            ast.keyword(
                arg="args",
                value=ast.Dict(
                    keys=[ast.Constant(value="arg1")],
                    values=[
                        ast.Call(
                            func=ast.Name(id="GraphQLArgument"),
                            args=[ast.Name(id="GraphQLString")],
                            keywords=[
                                ast.keyword(
                                    arg="default_value",
                                    value=ast.Constant(value="default_value"),
                                ),
                                ast.keyword(
                                    arg="description",
                                    value=ast.Constant(value="arg1_description"),
                                ),
                                ast.keyword(
                                    arg="deprecation_reason",
                                    value=ast.Constant(value=None),
                                ),
                            ],
                        )
                    ],
                ),
            ),
            ast.keyword(arg="description", value=ast.Constant(value="description")),
            ast.keyword(arg="deprecation_reason", value=ast.Constant(value="reason")),
        ],
    )

    assert compare_ast(generate_field(field, "type_map"), expected_ast)


@pytest.mark.parametrize(
    "type_,expected_ast",
    [
        (
            GraphQLObjectType(name="TestType", fields={}),
            ast.Call(
                func=ast.Name(id="cast"),
                args=[
                    ast.Name(id="GraphQLObjectType"),
                    ast.Subscript(
                        value=ast.Name(id="type_map"),
                        slice=ast.Constant(value="TestType"),
                    ),
                ],
                keywords=[],
            ),
        ),
        (
            GraphQLInterfaceType(name="TestInterFace", fields={}),
            ast.Call(
                func=ast.Name(id="cast"),
                args=[
                    ast.Name(id="GraphQLInterfaceType"),
                    ast.Subscript(
                        value=ast.Name(id="type_map"),
                        slice=ast.Constant(value="TestInterFace"),
                    ),
                ],
                keywords=[],
            ),
        ),
        (
            GraphQLUnionType(name="TestUnion", types=[]),
            ast.Call(
                func=ast.Name(id="cast"),
                args=[
                    ast.Name(id="GraphQLUnionType"),
                    ast.Subscript(
                        value=ast.Name(id="type_map"),
                        slice=ast.Constant(value="TestUnion"),
                    ),
                ],
                keywords=[],
            ),
        ),
        (
            GraphQLEnumType(name="TestEnum", values={}),
            ast.Call(
                func=ast.Name(id="cast"),
                args=[
                    ast.Name(id="GraphQLEnumType"),
                    ast.Subscript(
                        value=ast.Name(id="type_map"),
                        slice=ast.Constant(value="TestEnum"),
                    ),
                ],
                keywords=[],
            ),
        ),
        (
            GraphQLInputObjectType(name="TestInputType", fields={}),
            ast.Call(
                func=ast.Name(id="cast"),
                args=[
                    ast.Name(id="GraphQLInputObjectType"),
                    ast.Subscript(
                        value=ast.Name(id="type_map"),
                        slice=ast.Constant(value="TestInputType"),
                    ),
                ],
                keywords=[],
            ),
        ),
        (
            GraphQLScalarType(name="TestScalar"),
            ast.Call(
                func=ast.Name(id="cast"),
                args=[
                    ast.Name(id="GraphQLScalarType"),
                    ast.Subscript(
                        value=ast.Name(id="type_map"),
                        slice=ast.Constant(value="TestScalar"),
                    ),
                ],
                keywords=[],
            ),
        ),
        (GraphQLString, ast.Name(id="GraphQLString")),
        (GraphQLInt, ast.Name(id="GraphQLInt")),
        (GraphQLFloat, ast.Name(id="GraphQLFloat")),
        (GraphQLBoolean, ast.Name(id="GraphQLBoolean")),
        (GraphQLID, ast.Name(id="GraphQLID")),
        (
            GraphQLList(type_=GraphQLString),
            ast.Call(
                func=ast.Name(id="GraphQLList"),
                args=[ast.Name(id="GraphQLString")],
                keywords=[],
            ),
        ),
        (
            GraphQLNonNull(type_=GraphQLString),
            ast.Call(
                func=ast.Name(id="GraphQLNonNull"),
                args=[ast.Name(id="GraphQLString")],
                keywords=[],
            ),
        ),
    ],
)
def test_generate_field_type_returns_correct_ast_for_different_types(
    type_, expected_ast
):
    assert compare_ast(generate_field_type(type_, "type_map"), expected_ast)


def test_generate_args_returns_correct_dictionary():
    args = {
        "arg1": GraphQLArgument(
            type_=GraphQLString,
            default_value="default_value",
            description="arg_description",
        ),
        "arg2": GraphQLArgument(
            type_=GraphQLInputObjectType(
                name="InputTypeB", fields={"field1": GraphQLString}
            )
        ),
    }
    expected_dict = ast.Dict(
        keys=[ast.Constant(value="arg1"), ast.Constant(value="arg2")],
        values=[
            ast.Call(
                func=ast.Name(id="GraphQLArgument"),
                args=[ast.Name(id="GraphQLString")],
                keywords=[
                    ast.keyword(
                        arg="default_value", value=ast.Constant(value="default_value")
                    ),
                    ast.keyword(
                        arg="description", value=ast.Constant(value="arg_description")
                    ),
                    ast.keyword(
                        arg="deprecation_reason", value=ast.Constant(value=None)
                    ),
                ],
            ),
            ast.Call(
                func=ast.Name(id="GraphQLArgument"),
                args=[
                    ast.Call(
                        func=ast.Name(id="cast"),
                        args=[
                            ast.Name(id="GraphQLInputObjectType"),
                            ast.Subscript(
                                value=ast.Name(id="type_map"),
                                slice=ast.Constant(value="InputTypeB"),
                            ),
                        ],
                        keywords=[],
                    )
                ],
                keywords=[
                    ast.keyword(
                        arg="default_value", value=ast.Constant(value=Undefined)
                    ),
                    ast.keyword(arg="description", value=ast.Constant(value=None)),
                    ast.keyword(
                        arg="deprecation_reason", value=ast.Constant(value=None)
                    ),
                ],
            ),
        ],
    )

    assert compare_ast(generate_args(args, "type_map"), expected_dict)


def test_generate_arg_returns_correct_ast_call():
    arg = GraphQLArgument(
        type_=GraphQLInputObjectType(
            name="InputTypeA",
            fields={
                "field1": GraphQLString,
                "field2": GraphQLInputObjectType(name="SubInputTypeA", fields={}),
            },
        )
    )
    expected_ast = ast.Call(
        func=ast.Name(id="GraphQLArgument"),
        args=[
            ast.Call(
                func=ast.Name(id="cast"),
                args=[
                    ast.Name(id="GraphQLInputObjectType"),
                    ast.Subscript(
                        value=ast.Name(id="type_map"),
                        slice=ast.Constant(value="InputTypeA"),
                    ),
                ],
                keywords=[],
            )
        ],
        keywords=[
            ast.keyword(arg="default_value", value=ast.Constant(value=Undefined)),
            ast.keyword(arg="description", value=ast.Constant(value=None)),
            ast.keyword(arg="deprecation_reason", value=ast.Constant(value=None)),
        ],
    )

    assert compare_ast(generate_arg(arg, "type_map"), expected_ast)


def test_generate_enum_values_returns_dicitonary():
    values = {
        "X": GraphQLEnumValue(value="X"),
        "Y": GraphQLEnumValue(value="Y"),
        "Z": GraphQLEnumValue(value="Z"),
    }
    expected_ast = ast.Dict(
        keys=[
            ast.Constant(value="X"),
            ast.Constant(value="Y"),
            ast.Constant(value="Z"),
        ],
        values=[
            ast.Call(
                func=ast.Name(id="GraphQLEnumValue"),
                args=[],
                keywords=[
                    ast.keyword(arg="value", value=ast.Constant(value="X")),
                    ast.keyword(arg="description", value=ast.Constant(value=None)),
                    ast.keyword(
                        arg="deprecation_reason", value=ast.Constant(value=None)
                    ),
                ],
            ),
            ast.Call(
                func=ast.Name(id="GraphQLEnumValue"),
                args=[],
                keywords=[
                    ast.keyword(arg="value", value=ast.Constant(value="Y")),
                    ast.keyword(arg="description", value=ast.Constant(value=None)),
                    ast.keyword(
                        arg="deprecation_reason", value=ast.Constant(value=None)
                    ),
                ],
            ),
            ast.Call(
                func=ast.Name(id="GraphQLEnumValue"),
                args=[],
                keywords=[
                    ast.keyword(arg="value", value=ast.Constant(value="Z")),
                    ast.keyword(arg="description", value=ast.Constant(value=None)),
                    ast.keyword(
                        arg="deprecation_reason", value=ast.Constant(value=None)
                    ),
                ],
            ),
        ],
    )

    assert compare_ast(generate_enum_values(values), expected_ast)


def test_generate_enum_value_returns_correct_ast_call():
    value = GraphQLEnumValue(value="X", description="desc", deprecation_reason="reason")
    expected_ast = ast.Call(
        func=ast.Name(id="GraphQLEnumValue"),
        args=[],
        keywords=[
            ast.keyword(arg="value", value=ast.Constant(value="X")),
            ast.keyword(arg="description", value=ast.Constant(value="desc")),
            ast.keyword(arg="deprecation_reason", value=ast.Constant(value="reason")),
        ],
    )

    assert compare_ast(generate_enum_value(value), expected_ast)


def test_generate_input_field_map_returns_lambda():
    field_map = {
        "field1": GraphQLInputField(
            type_=GraphQLInputObjectType(name="TestInputA", fields={}),
            default_value="default",
            description="desc",
            deprecation_reason="reason",
        ),
        "field2": GraphQLInputField(type_=GraphQLFloat),
    }
    expected_ast = ast.Lambda(
        args=ast.arguments(
            posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]
        ),
        body=ast.Dict(
            keys=[ast.Constant(value="field1"), ast.Constant(value="field2")],
            values=[
                ast.Call(
                    func=ast.Name(id="GraphQLInputField"),
                    args=[
                        ast.Call(
                            func=ast.Name(id="cast"),
                            args=[
                                ast.Name(id="GraphQLInputObjectType"),
                                ast.Subscript(
                                    value=ast.Name(id="type_map"),
                                    slice=ast.Constant(value="TestInputA"),
                                ),
                            ],
                            keywords=[],
                        )
                    ],
                    keywords=[
                        ast.keyword(
                            arg="default_value", value=ast.Constant(value="default")
                        ),
                        ast.keyword(
                            arg="description", value=ast.Constant(value="desc")
                        ),
                        ast.keyword(
                            arg="deprecation_reason", value=ast.Constant(value="reason")
                        ),
                    ],
                ),
                ast.Call(
                    func=ast.Name(id="GraphQLInputField"),
                    args=[ast.Name(id="GraphQLFloat")],
                    keywords=[
                        ast.keyword(
                            arg="default_value", value=ast.Constant(value=Undefined)
                        ),
                        ast.keyword(arg="description", value=ast.Constant(value=None)),
                        ast.keyword(
                            arg="deprecation_reason", value=ast.Constant(value=None)
                        ),
                    ],
                ),
            ],
        ),
    )

    assert compare_ast(generate_input_field_map(field_map, "type_map"), expected_ast)


def test_generate_input_field_returns_ast_call():
    field = GraphQLInputField(
        type_=GraphQLInputObjectType(name="TestInputA", fields={}),
        default_value="default",
        description="desc",
        deprecation_reason="reason",
    )
    expected_ast = ast.Call(
        func=ast.Name(id="GraphQLInputField"),
        args=[
            ast.Call(
                func=ast.Name(id="cast"),
                args=[
                    ast.Name(id="GraphQLInputObjectType"),
                    ast.Subscript(
                        value=ast.Name(id="type_map"),
                        slice=ast.Constant(value="TestInputA"),
                    ),
                ],
                keywords=[],
            )
        ],
        keywords=[
            ast.keyword(arg="default_value", value=ast.Constant(value="default")),
            ast.keyword(arg="description", value=ast.Constant(value="desc")),
            ast.keyword(arg="deprecation_reason", value=ast.Constant(value="reason")),
        ],
    )

    assert compare_ast(generate_input_field(field, "type_map"), expected_ast)
