import ast

import pytest
from graphql import (
    GraphQLEnumType,
    GraphQLEnumValue,
    GraphQLField,
    GraphQLFloat,
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLInterfaceType,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLString,
    GraphQLUnionType,
    Undefined,
)

from ariadne_codegen.graphql_schema_generators.named_types import (
    generate_enum_type,
    generate_input_object_type,
    generate_interface_type,
    generate_named_type,
    generate_object_type,
    generate_scalar_type,
    generate_union_type,
)

from ..utils import compare_ast


@pytest.mark.parametrize(
    "type_,method_name",
    [
        (GraphQLScalarType("TestScalar"), "generate_scalar_type"),
        (GraphQLObjectType("TestType", fields={}), "generate_object_type"),
        (GraphQLInterfaceType("TestInterface", fields={}), "generate_interface_type"),
        (GraphQLUnionType("TestUnion", types=[]), "generate_union_type"),
        (GraphQLEnumType("TestEnum", values={}), "generate_enum_type"),
        (GraphQLInputObjectType("TestInput", fields={}), "generate_input_object_type"),
    ],
)
def test_generate_named_type_calls_correct_method(type_, method_name, mocker):
    mocked_method = mocker.patch(
        f"ariadne_codegen.graphql_schema_generators.named_types.{method_name}"
    )

    generate_named_type(type_, "type_map")

    assert mocked_method.called


def test_generate_scalar_type_returns_ast_call():
    scalar_type = GraphQLScalarType(
        "TestScalar", description="scalar desc", specified_by_url="scalar url"
    )
    expected_ast = ast.Call(
        func=ast.Name(id="GraphQLScalarType"),
        args=[],
        keywords=[
            ast.keyword(arg="name", value=ast.Constant(value="TestScalar")),
            ast.keyword(arg="description", value=ast.Constant(value="scalar desc")),
            ast.keyword(arg="specified_by_url", value=ast.Constant(value="scalar url")),
        ],
    )

    assert compare_ast(generate_scalar_type(scalar_type), expected_ast)


def test_generate_object_type_returns_ast_call():
    object_type = GraphQLObjectType(
        "TestTypeA",
        fields={
            "fieldB": GraphQLField(
                GraphQLObjectType(name="TestTypeB", fields={}),
                description="description",
                deprecation_reason="reason",
            ),
            "fieldC": GraphQLField(GraphQLString),
        },
        interfaces=[
            GraphQLInterfaceType("InterfaceX", fields={}),
            GraphQLInterfaceType("InterfaceY", fields={}),
        ],
        description="type desc",
    )
    expected_ast = ast.Call(
        func=ast.Name(id="GraphQLObjectType"),
        args=[],
        keywords=[
            ast.keyword(arg="name", value=ast.Constant(value="TestTypeA")),
            ast.keyword(arg="description", value=ast.Constant(value="type desc")),
            ast.keyword(
                arg="interfaces",
                value=ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[],
                    ),
                    body=ast.Call(
                        func=ast.Name(id="cast"),
                        args=[
                            ast.Subscript(
                                value=ast.Name(id="List"),
                                slice=ast.Name(id="GraphQLInterfaceType"),
                            ),
                            ast.List(
                                elts=[
                                    ast.Subscript(
                                        value=ast.Name(id="type_map"),
                                        slice=ast.Constant(value="InterfaceX"),
                                    ),
                                    ast.Subscript(
                                        value=ast.Name(id="type_map"),
                                        slice=ast.Constant(value="InterfaceY"),
                                    ),
                                ]
                            ),
                        ],
                        keywords=[],
                    ),
                ),
            ),
            ast.keyword(
                arg="fields",
                value=ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[],
                    ),
                    body=ast.Dict(
                        keys=[
                            ast.Constant(value="fieldB"),
                            ast.Constant(value="fieldC"),
                        ],
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
                                                slice=ast.Constant(value="TestTypeB"),
                                            ),
                                        ],
                                        keywords=[],
                                    )
                                ],
                                keywords=[
                                    ast.keyword(
                                        arg="args", value=ast.Dict(keys=[], values=[])
                                    ),
                                    ast.keyword(
                                        arg="description",
                                        value=ast.Constant(value="description"),
                                    ),
                                    ast.keyword(
                                        arg="deprecation_reason",
                                        value=ast.Constant(value="reason"),
                                    ),
                                ],
                            ),
                            ast.Call(
                                func=ast.Name(id="GraphQLField"),
                                args=[ast.Name(id="GraphQLString")],
                                keywords=[
                                    ast.keyword(
                                        arg="args", value=ast.Dict(keys=[], values=[])
                                    ),
                                    ast.keyword(
                                        arg="description",
                                        value=ast.Constant(value=None),
                                    ),
                                    ast.keyword(
                                        arg="deprecation_reason",
                                        value=ast.Constant(value=None),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            ),
        ],
    )

    assert compare_ast(generate_object_type(object_type, "type_map"), expected_ast)


def test_generate_interface_type_returns_ast_call():
    interface_type = GraphQLInterfaceType(
        "TestInterfaceA",
        fields={
            "fieldB": GraphQLField(
                GraphQLInterfaceType(name="TestInterfaceB", fields={}),
                description="description",
                deprecation_reason="reason",
            ),
            "fieldC": GraphQLField(GraphQLString),
        },
        interfaces=[
            GraphQLInterfaceType("InterfaceX", fields={}),
            GraphQLInterfaceType("InterfaceY", fields={}),
        ],
        description="interface desc",
    )
    expected_ast = ast.Call(
        func=ast.Name(id="GraphQLInterfaceType"),
        args=[],
        keywords=[
            ast.keyword(arg="name", value=ast.Constant(value="TestInterfaceA")),
            ast.keyword(arg="description", value=ast.Constant(value="interface desc")),
            ast.keyword(
                arg="interfaces",
                value=ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[],
                    ),
                    body=ast.Call(
                        func=ast.Name(id="cast"),
                        args=[
                            ast.Subscript(
                                value=ast.Name(id="List"),
                                slice=ast.Name(id="GraphQLInterfaceType"),
                            ),
                            ast.List(
                                elts=[
                                    ast.Subscript(
                                        value=ast.Name(id="type_map"),
                                        slice=ast.Constant(value="InterfaceX"),
                                    ),
                                    ast.Subscript(
                                        value=ast.Name(id="type_map"),
                                        slice=ast.Constant(value="InterfaceY"),
                                    ),
                                ]
                            ),
                        ],
                        keywords=[],
                    ),
                ),
            ),
            ast.keyword(
                arg="fields",
                value=ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[],
                    ),
                    body=ast.Dict(
                        keys=[
                            ast.Constant(value="fieldB"),
                            ast.Constant(value="fieldC"),
                        ],
                        values=[
                            ast.Call(
                                func=ast.Name(id="GraphQLField"),
                                args=[
                                    ast.Call(
                                        func=ast.Name(id="cast"),
                                        args=[
                                            ast.Name(id="GraphQLInterfaceType"),
                                            ast.Subscript(
                                                value=ast.Name(id="type_map"),
                                                slice=ast.Constant(
                                                    value="TestInterfaceB"
                                                ),
                                            ),
                                        ],
                                        keywords=[],
                                    )
                                ],
                                keywords=[
                                    ast.keyword(
                                        arg="args", value=ast.Dict(keys=[], values=[])
                                    ),
                                    ast.keyword(
                                        arg="description",
                                        value=ast.Constant(value="description"),
                                    ),
                                    ast.keyword(
                                        arg="deprecation_reason",
                                        value=ast.Constant(value="reason"),
                                    ),
                                ],
                            ),
                            ast.Call(
                                func=ast.Name(id="GraphQLField"),
                                args=[ast.Name(id="GraphQLString")],
                                keywords=[
                                    ast.keyword(
                                        arg="args", value=ast.Dict(keys=[], values=[])
                                    ),
                                    ast.keyword(
                                        arg="description",
                                        value=ast.Constant(value=None),
                                    ),
                                    ast.keyword(
                                        arg="deprecation_reason",
                                        value=ast.Constant(value=None),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            ),
        ],
    )

    assert compare_ast(
        generate_interface_type(interface_type, "type_map"), expected_ast
    )


def test_generate_union_type_returns_ast_call():
    union_type = GraphQLUnionType(
        "TestUnion",
        types=[
            GraphQLObjectType("TestTypeA", fields={}),
            GraphQLObjectType("TestTypeB", fields={}),
        ],
        description="union desc",
    )
    expected_ast = ast.Call(
        func=ast.Name(id="GraphQLUnionType"),
        args=[],
        keywords=[
            ast.keyword(arg="name", value=ast.Constant(value="TestUnion")),
            ast.keyword(arg="description", value=ast.Constant(value="union desc")),
            ast.keyword(
                arg="types",
                value=ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[],
                    ),
                    body=ast.Call(
                        func=ast.Name(id="cast"),
                        args=[
                            ast.Subscript(
                                value=ast.Name(id="List"),
                                slice=ast.Name(id="GraphQLObjectType"),
                            ),
                            ast.List(
                                elts=[
                                    ast.Subscript(
                                        value=ast.Name(id="type_map"),
                                        slice=ast.Constant(value="TestTypeA"),
                                    ),
                                    ast.Subscript(
                                        value=ast.Name(id="type_map"),
                                        slice=ast.Constant(value="TestTypeB"),
                                    ),
                                ]
                            ),
                        ],
                        keywords=[],
                    ),
                ),
            ),
        ],
    )

    assert compare_ast(generate_union_type(union_type, "type_map"), expected_ast)


def test_generate_enum_type_returns_ast_call():
    enum_type = GraphQLEnumType(
        "TestEnum",
        values={
            "X": GraphQLEnumValue(value="X"),
            "Y": GraphQLEnumValue(value="Y"),
            "Z": GraphQLEnumValue(value="Z"),
        },
        description="enum desc",
    )
    expected_ast = ast.Call(
        func=ast.Name(id="GraphQLEnumType"),
        args=[],
        keywords=[
            ast.keyword(arg="name", value=ast.Constant(value="TestEnum")),
            ast.keyword(arg="description", value=ast.Constant(value="enum desc")),
            ast.keyword(
                arg="values",
                value=ast.Dict(
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
                                ast.keyword(
                                    arg="description", value=ast.Constant(value=None)
                                ),
                                ast.keyword(
                                    arg="deprecation_reason",
                                    value=ast.Constant(value=None),
                                ),
                            ],
                        ),
                        ast.Call(
                            func=ast.Name(id="GraphQLEnumValue"),
                            args=[],
                            keywords=[
                                ast.keyword(arg="value", value=ast.Constant(value="Y")),
                                ast.keyword(
                                    arg="description", value=ast.Constant(value=None)
                                ),
                                ast.keyword(
                                    arg="deprecation_reason",
                                    value=ast.Constant(value=None),
                                ),
                            ],
                        ),
                        ast.Call(
                            func=ast.Name(id="GraphQLEnumValue"),
                            args=[],
                            keywords=[
                                ast.keyword(arg="value", value=ast.Constant(value="Z")),
                                ast.keyword(
                                    arg="description", value=ast.Constant(value=None)
                                ),
                                ast.keyword(
                                    arg="deprecation_reason",
                                    value=ast.Constant(value=None),
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )

    assert compare_ast(generate_enum_type(enum_type), expected_ast)


def test_generate_input_object_type_returns_ast_call():
    input_type = GraphQLInputObjectType(
        "TestInputA",
        fields={
            "field1": GraphQLInputField(
                type_=GraphQLInputObjectType(name="TestInputB", fields={}),
                default_value="default",
                description="desc",
                deprecation_reason="reason",
            ),
            "field2": GraphQLInputField(type_=GraphQLFloat),
        },
        description="input desc",
    )
    expected_ast = ast.Call(
        func=ast.Name(id="GraphQLInputObjectType"),
        args=[],
        keywords=[
            ast.keyword(arg="name", value=ast.Constant(value="TestInputA")),
            ast.keyword(arg="description", value=ast.Constant(value="input desc")),
            ast.keyword(
                arg="fields",
                value=ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[],
                    ),
                    body=ast.Dict(
                        keys=[
                            ast.Constant(value="field1"),
                            ast.Constant(value="field2"),
                        ],
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
                                                slice=ast.Constant(value="TestInputB"),
                                            ),
                                        ],
                                        keywords=[],
                                    )
                                ],
                                keywords=[
                                    ast.keyword(
                                        arg="default_value",
                                        value=ast.Constant(value="default"),
                                    ),
                                    ast.keyword(
                                        arg="description",
                                        value=ast.Constant(value="desc"),
                                    ),
                                    ast.keyword(
                                        arg="deprecation_reason",
                                        value=ast.Constant(value="reason"),
                                    ),
                                ],
                            ),
                            ast.Call(
                                func=ast.Name(id="GraphQLInputField"),
                                args=[ast.Name(id="GraphQLFloat")],
                                keywords=[
                                    ast.keyword(
                                        arg="default_value",
                                        value=ast.Constant(value=Undefined),
                                    ),
                                    ast.keyword(
                                        arg="description",
                                        value=ast.Constant(value=None),
                                    ),
                                    ast.keyword(
                                        arg="deprecation_reason",
                                        value=ast.Constant(value=None),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            ),
        ],
    )

    assert compare_ast(generate_input_object_type(input_type, "type_map"), expected_ast)
