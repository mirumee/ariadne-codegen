import ast
from typing import Union

from graphql import (
    GraphQLArgument,
    GraphQLArgumentMap,
    GraphQLEnumType,
    GraphQLEnumValue,
    GraphQLEnumValueMap,
    GraphQLField,
    GraphQLFieldMap,
    GraphQLInputField,
    GraphQLInputFieldMap,
    GraphQLInputObjectType,
    GraphQLInputType,
    GraphQLInterfaceType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLOutputType,
    GraphQLScalarType,
    GraphQLUnionType,
)

from ..codegen import (
    generate_call,
    generate_constant,
    generate_dict,
    generate_keyword,
    generate_lambda,
    generate_name,
)
from ..exceptions import NotSupported
from .constants import STANDARD_SCALARS
from .utils import get_named_type


def generate_field_map(
    fields: GraphQLFieldMap, type_map_name: str
) -> Union[ast.Lambda, ast.Constant]:
    if not fields:
        return generate_constant({})

    fields_dict = generate_dict()
    for name, field in fields.items():
        fields_dict.keys.append(generate_constant(name))
        fields_dict.values.append(generate_field(field, type_map_name))

    return generate_lambda(body=fields_dict)


def generate_field(field: GraphQLField, type_map_name: str) -> ast.Call:
    return generate_call(
        func=generate_name("GraphQLField"),
        args=[generate_field_type(field.type, type_map_name)],
        keywords=[
            generate_keyword(
                value=generate_args(field.args, type_map_name), arg="args"
            ),
            generate_keyword(
                value=generate_constant(field.description), arg="description"
            ),
            generate_keyword(
                value=generate_constant(field.deprecation_reason),
                arg="deprecation_reason",
            ),
        ],
    )


def generate_field_type(
    type_: Union[GraphQLOutputType, GraphQLInputType], type_map_name: str
) -> Union[ast.Call, ast.Name]:
    if isinstance(
        type_,
        (
            GraphQLObjectType,
            GraphQLInterfaceType,
            GraphQLUnionType,
            GraphQLEnumType,
            GraphQLInputObjectType,
        ),
    ):
        return get_named_type(type_, type_map_name)

    if isinstance(type_, GraphQLScalarType):
        if type_.name in STANDARD_SCALARS:
            return generate_name(STANDARD_SCALARS[type_.name])

        return get_named_type(type_, type_map_name)
    if isinstance(type_, GraphQLList):
        return generate_call(
            func=generate_name("GraphQLList"),
            args=[generate_field_type(type_.of_type, type_map_name)],
        )

    if isinstance(type_, GraphQLNonNull):
        return generate_call(
            func=generate_name("GraphQLNonNull"),
            args=[generate_field_type(type_.of_type, type_map_name)],
        )

    raise NotSupported(f"Unknown field type: {type(type_)}")


def generate_args(args: GraphQLArgumentMap, type_map_name: str) -> ast.Dict:
    args_dict = generate_dict()
    for name, arg in args.items():
        args_dict.keys.append(generate_constant(name))
        args_dict.values.append(generate_arg(arg, type_map_name))
    return args_dict


def generate_arg(arg: GraphQLArgument, type_map_name: str) -> ast.Call:
    return generate_call(
        func=generate_name("GraphQLArgument"),
        args=[generate_field_type(arg.type, type_map_name)],
        keywords=[
            generate_keyword(
                value=generate_constant(arg.default_value), arg="default_value"
            ),
            generate_keyword(
                value=generate_constant(arg.description),
                arg="description",
            ),
            generate_keyword(
                value=generate_constant(arg.deprecation_reason),
                arg="deprecation_reason",
            ),
        ],
    )


def generate_enum_values(values: GraphQLEnumValueMap) -> ast.Dict:
    values_dict = generate_dict()
    for name, value in values.items():
        values_dict.keys.append(generate_constant(name))
        values_dict.values.append(generate_enum_value(value))
    return values_dict


def generate_enum_value(value: GraphQLEnumValue) -> ast.Call:
    return generate_call(
        func=generate_name("GraphQLEnumValue"),
        keywords=[
            generate_keyword(value=generate_constant(value.value), arg="value"),
            generate_keyword(
                value=generate_constant(value.description), arg="description"
            ),
            generate_keyword(
                value=generate_constant(value.deprecation_reason),
                arg="deprecation_reason",
            ),
        ],
    )


def generate_input_field_map(
    input_fields: GraphQLInputFieldMap, type_map_name: str
) -> Union[ast.Lambda, ast.Constant]:
    if not input_fields:
        return generate_constant({})

    input_fields_dict = generate_dict()
    for name, input_field in input_fields.items():
        input_fields_dict.keys.append(generate_constant(name))
        input_fields_dict.values.append(
            generate_input_field(input_field, type_map_name)
        )

    return generate_lambda(body=input_fields_dict)


def generate_input_field(
    input_field: GraphQLInputField, type_map_name: str
) -> ast.Call:
    return generate_call(
        func=generate_name("GraphQLInputField"),
        args=[generate_field_type(input_field.type, type_map_name)],
        keywords=[
            generate_keyword(
                value=generate_constant(input_field.default_value), arg="default_value"
            ),
            generate_keyword(
                value=generate_constant(input_field.description), arg="description"
            ),
            generate_keyword(
                value=generate_constant(input_field.deprecation_reason),
                arg="deprecation_reason",
            ),
        ],
    )
