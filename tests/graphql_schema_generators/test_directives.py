import ast

import pytest
from graphql import (
    DirectiveLocation,
    GraphQLArgument,
    GraphQLDirective,
    GraphQLInputObjectType,
    GraphQLString,
    Undefined,
)

from ariadne_codegen.graphql_schema_generators.directives import (
    generate_directive,
    generate_directive_location,
    generate_directive_locations,
)

from ..utils import compare_ast


def test_generate_directive_returns_correct_ast_call():
    directive = GraphQLDirective(
        name="DirectiveA",
        locations=[DirectiveLocation.FIELD, DirectiveLocation.SCALAR],
        args={
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
        },
        is_repeatable=False,
        description="description",
    )
    expected_ast = ast.Call(
        func=ast.Name(id="GraphQLDirective"),
        args=[],
        keywords=[
            ast.keyword(arg="name", value=ast.Constant(value="DirectiveA")),
            ast.keyword(arg="description", value=ast.Constant(value="description")),
            ast.keyword(arg="is_repeatable", value=ast.Constant(value=False)),
            ast.keyword(
                arg="locations",
                value=ast.Tuple(
                    elts=[
                        ast.Attribute(
                            value=ast.Name(id="DirectiveLocation"), attr="FIELD"
                        ),
                        ast.Attribute(
                            value=ast.Name(id="DirectiveLocation"), attr="SCALAR"
                        ),
                    ]
                ),
            ),
            ast.keyword(
                arg="args",
                value=ast.Dict(
                    keys=[ast.Constant(value="arg1"), ast.Constant(value="arg2")],
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
                                    value=ast.Constant(value="arg_description"),
                                ),
                                ast.keyword(
                                    arg="deprecation_reason",
                                    value=ast.Constant(value=None),
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
                                    arg="default_value",
                                    value=ast.Constant(value=Undefined),
                                ),
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

    assert compare_ast(generate_directive(directive, "type_map"), expected_ast)


def test_generate_directive_locations_returns_tuple_with_correct_locations_asts():
    assert compare_ast(
        generate_directive_locations(
            [DirectiveLocation.FIELD, DirectiveLocation.SCALAR]
        ),
        ast.Tuple(
            elts=[
                ast.Attribute(value=ast.Name(id="DirectiveLocation"), attr="FIELD"),
                ast.Attribute(value=ast.Name(id="DirectiveLocation"), attr="SCALAR"),
            ]
        ),
    )


@pytest.mark.parametrize("location", list(DirectiveLocation))
def test_generate_directive_location_returns_correct_ast_representation(location):
    assert compare_ast(
        generate_directive_location(location),
        ast.Attribute(value=ast.Name(id="DirectiveLocation"), attr=location.name),
    )
