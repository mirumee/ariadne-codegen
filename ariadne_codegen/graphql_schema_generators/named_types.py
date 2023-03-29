import ast
from typing import Callable, Dict, Type

from graphql import (
    GraphQLEnumType,
    GraphQLInputObjectType,
    GraphQLInterfaceType,
    GraphQLNamedType,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLUnionType,
)

from ..codegen import generate_call, generate_constant, generate_keyword, generate_name
from ..exceptions import NotSupported
from .fields import generate_enum_values, generate_field_map, generate_input_field_map
from .utils import get_list_of_named_types


def generate_named_type(type_: GraphQLNamedType, type_map_name: str) -> ast.Call:
    generate_methods_map: Dict[Type, Callable[..., ast.Call]] = {
        GraphQLScalarType: generate_scalar_type,
        GraphQLObjectType: generate_object_type,
        GraphQLInterfaceType: generate_interface_type,
        GraphQLUnionType: generate_union_type,
        GraphQLEnumType: generate_enum_type,
        GraphQLInputObjectType: generate_input_object_type,
    }
    generate_method = generate_methods_map.get(type(type_), None)
    if not generate_method:
        raise NotSupported(f"Unknown type: {type(type_)}")

    return generate_method(type_, type_map_name)


def generate_scalar_type(type_: GraphQLScalarType, *_) -> ast.Call:
    return generate_call(
        func=generate_name("GraphQLScalarType"),
        keywords=[
            generate_keyword(arg="name", value=generate_constant(type_.name)),
            generate_keyword(
                arg="description", value=generate_constant(type_.description)
            ),
            generate_keyword(
                arg="specified_by_url", value=generate_constant(type_.specified_by_url)
            ),
        ],
    )


def generate_object_type(type_: GraphQLObjectType, type_map_name: str) -> ast.Call:
    return generate_call(
        func=generate_name("GraphQLObjectType"),
        keywords=[
            generate_keyword(arg="name", value=generate_constant(type_.name)),
            generate_keyword(
                arg="description", value=generate_constant(type_.description)
            ),
            generate_keyword(
                arg="interfaces",
                value=get_list_of_named_types(
                    [i.name for i in type_.interfaces],
                    type_map_name,
                    GraphQLInterfaceType.__name__,
                ),
            ),
            generate_keyword(
                arg="fields", value=generate_field_map(type_.fields, type_map_name)
            ),
        ],
    )


def generate_interface_type(
    type_: GraphQLInterfaceType, type_map_name: str
) -> ast.Call:
    return generate_call(
        func=generate_name("GraphQLInterfaceType"),
        keywords=[
            generate_keyword(arg="name", value=generate_constant(type_.name)),
            generate_keyword(
                arg="description", value=generate_constant(type_.description)
            ),
            generate_keyword(
                arg="interfaces",
                value=get_list_of_named_types(
                    [i.name for i in type_.interfaces],
                    type_map_name,
                    GraphQLInterfaceType.__name__,
                ),
            ),
            generate_keyword(
                arg="fields", value=generate_field_map(type_.fields, type_map_name)
            ),
        ],
    )


def generate_union_type(type_: GraphQLUnionType, type_map_name: str) -> ast.Call:
    return generate_call(
        func=generate_name("GraphQLUnionType"),
        keywords=[
            generate_keyword(arg="name", value=generate_constant(type_.name)),
            generate_keyword(
                arg="description", value=generate_constant(type_.description)
            ),
            generate_keyword(
                arg="types",
                value=get_list_of_named_types(
                    [t.name for t in type_.types],
                    type_map_name,
                    GraphQLObjectType.__name__,
                ),
            ),
        ],
    )


def generate_enum_type(type_: GraphQLEnumType, *_) -> ast.Call:
    return generate_call(
        func=generate_name("GraphQLEnumType"),
        keywords=[
            generate_keyword(arg="name", value=generate_constant(type_.name)),
            generate_keyword(
                arg="description", value=generate_constant(type_.description)
            ),
            generate_keyword(arg="values", value=generate_enum_values(type_.values)),
        ],
    )


def generate_input_object_type(
    type_: GraphQLInputObjectType, type_map_name: str
) -> ast.Call:
    return generate_call(
        func=generate_name("GraphQLInputObjectType"),
        keywords=[
            generate_keyword(arg="name", value=generate_constant(type_.name)),
            generate_keyword(
                arg="description", value=generate_constant(type_.description)
            ),
            generate_keyword(
                arg="fields",
                value=generate_input_field_map(type_.fields, type_map_name),
            ),
        ],
    )
