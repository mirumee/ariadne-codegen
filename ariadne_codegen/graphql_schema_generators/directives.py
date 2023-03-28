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
            generate_keyword(arg="name", value=generate_constant(directive.name)),
            generate_keyword(
                arg="description", value=generate_constant(directive.description)
            ),
            generate_keyword(
                arg="is_repeatable", value=generate_constant(directive.is_repeatable)
            ),
            generate_keyword(
                arg="locations", value=generate_directive_locations(directive.locations)
            ),
            generate_keyword(arg="args", value=args),
        ],
    )


def generate_directive_locations(locations: Collection[DirectiveLocation]) -> ast.Tuple:
    return generate_tuple(elts=[generate_directive_location(loc) for loc in locations])


def generate_directive_location(location: DirectiveLocation) -> ast.Attribute:
    return generate_attribute(
        value=generate_name("DirectiveLocation"), attr=location.name
    )
