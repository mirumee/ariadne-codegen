import ast
from typing import List, Optional, Union

from graphql import GraphQLNamedType

from ..codegen import (
    generate_call,
    generate_constant,
    generate_lambda,
    generate_list,
    generate_name,
    generate_subscript,
)


def get_named_type(type_: GraphQLNamedType, type_map_name: str) -> ast.Call:
    return generate_call(
        func=generate_name("cast"),
        args=[
            generate_name(type_.__class__.__name__),
            generate_subscript(
                value=generate_name(type_map_name),
                slice_=generate_constant(type_.name),
            ),
        ],
    )


def get_optional_named_type(
    type_: Optional[GraphQLNamedType], type_map_name: str
) -> Union[ast.Constant, ast.Call]:
    if not type_:
        return generate_constant(None)

    return get_named_type(type_=type_, type_map_name=type_map_name)


def get_list_of_named_types(
    types_names: List[str], type_map_name: str, list_element_annotation: str
) -> Union[ast.Lambda, ast.Constant]:
    if not types_names:
        return generate_constant([])

    return generate_lambda(
        body=generate_call(
            func=generate_name("cast"),
            args=[
                generate_subscript(
                    value=generate_name("List"),
                    slice_=generate_name(list_element_annotation),
                ),
                generate_list(
                    elements=[
                        generate_subscript(
                            value=generate_name(type_map_name),
                            slice_=generate_constant(name),
                        )
                        for name in types_names
                    ]
                ),
            ],
        )
    )
