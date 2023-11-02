import ast
from typing import Collection

from graphql import DirectiveLocation, GraphQLDirective

from ..codegen import (
    generate_attribute,
    generate_call,
    generate_constant,
    generate_keyword,
    generate_name,
    generate_tuple,
)
from .fields import generate_args


def generate_directive(directive: GraphQLDirective, type_map_name: str) -> ast.Call:
    args = (
        generate_args(directive.args, type_map_name)
        if directive.args
        else generate_constant(None)
    )
    return generate_call(
        func=generate_name("GraphQLDirective"),
        keywords=[
            generate_keyword(value=generate_constant(directive.name), arg="name"),
            generate_keyword(
                value=generate_constant(directive.description), arg="description"
            ),
            generate_keyword(
                value=generate_constant(directive.is_repeatable), arg="is_repeatable"
            ),
            generate_keyword(
                value=generate_directive_locations(directive.locations), arg="locations"
            ),
            generate_keyword(value=args, arg="args"),
        ],
    )


def generate_directive_locations(locations: Collection[DirectiveLocation]) -> ast.Tuple:
    return generate_tuple(elts=[generate_directive_location(loc) for loc in locations])


def generate_directive_location(location: DirectiveLocation) -> ast.Attribute:
    return generate_attribute(
        value=generate_name("DirectiveLocation"), attr=location.name
    )
