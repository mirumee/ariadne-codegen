import ast
from pathlib import Path

from graphql import GraphQLSchema
from graphql.type.schema import TypeMap

from ..codegen import (
    generate_ann_assign,
    generate_attribute,
    generate_call,
    generate_constant,
    generate_dict,
    generate_import_from,
    generate_keyword,
    generate_list,
    generate_module,
    generate_name,
)
from ..utils import ast_to_str
from .constants import STANDARD_TYPES
from .directives import generate_directive
from .named_types import generate_named_type
from .utils import get_optional_named_type


def generate_graphql_schema_file(
    schema: GraphQLSchema,
    target_file_path: str,
    type_map_name: str,
    schema_variable_name: str,
):
    module = generate_schema_module(
        schema,
        type_map_name=type_map_name,
        schema_variable_name=schema_variable_name,
    )
    code = ast_to_str(module)
    Path(target_file_path).write_text(code, encoding="UTF-8")


def generate_schema_module(
    schema: GraphQLSchema, type_map_name: str, schema_variable_name: str
) -> ast.Module:
    return generate_module(
        body=[
            generate_import_from(
                names=[
                    "DirectiveLocation",
                    "GraphQLArgument",
                    "GraphQLDirective",
                    "GraphQLEnumType",
                    "GraphQLEnumValue",
                    "GraphQLField",
                    "GraphQLInputField",
                    "GraphQLInputObjectType",
                    "GraphQLInterfaceType",
                    "GraphQLList",
                    "GraphQLNamedType",
                    "GraphQLNonNull",
                    "GraphQLObjectType",
                    "GraphQLScalarType",
                    "GraphQLSchema",
                    "GraphQLUnionType",
                    "GraphQLID",
                    "GraphQLInt",
                    "GraphQLFloat",
                    "GraphQLString",
                    "GraphQLBoolean",
                    "Undefined",
                ],
                from_="graphql",
            ),
            generate_import_from(
                names=["TypeMap"],
                from_="graphql.type.schema",
            ),
            generate_import_from(names=["cast", "List"], from_="typing"),
            generate_ann_assign(
                target=type_map_name,
                annotation=generate_name("TypeMap"),
                value=generate_type_map(schema.type_map, type_map_name),
            ),
            generate_ann_assign(
                target=schema_variable_name,
                annotation=generate_name("GraphQLSchema"),
                value=generate_schema(schema, type_map_name),
            ),
        ]
    )


def generate_type_map(type_map: TypeMap, type_map_name: str) -> ast.Dict:
    type_map_dict = generate_dict()
    for name, type_ in type_map.items():
        if name not in STANDARD_TYPES:
            type_map_dict.keys.append(generate_constant(name))
            type_map_dict.values.append(generate_named_type(type_, type_map_name))

    return type_map_dict


def generate_schema(schema: GraphQLSchema, type_map_name: str) -> ast.Call:
    return generate_call(
        func=generate_name("GraphQLSchema"),
        keywords=[
            generate_keyword(
                arg="query",
                value=get_optional_named_type(schema.query_type, type_map_name),
            ),
            generate_keyword(
                arg="mutation",
                value=get_optional_named_type(schema.mutation_type, type_map_name),
            ),
            generate_keyword(
                arg="subscription",
                value=get_optional_named_type(schema.subscription_type, type_map_name),
            ),
            generate_keyword(
                arg="types",
                value=generate_call(
                    func=generate_attribute(
                        value=generate_name(type_map_name), attr="values"
                    ),
                ),
            ),
            generate_keyword(
                arg="directives",
                value=generate_list(
                    elements=[
                        generate_directive(d, type_map_name) for d in schema.directives
                    ]
                ),
            ),
            generate_keyword(
                arg="description", value=generate_constant(schema.description)
            ),
        ],
    )
