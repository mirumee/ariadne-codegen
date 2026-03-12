from typing import cast

from graphql import (
    DirectiveLocation,
    GraphQLArgument,
    GraphQLBoolean,
    GraphQLDirective,
    GraphQLEnumType,
    GraphQLEnumValue,
    GraphQLField,
    GraphQLFloat,
    GraphQLID,
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLInt,
    GraphQLInterfaceType,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLSchema,
    GraphQLString,
    GraphQLUnionType,
    Undefined,
)
from graphql.type.schema import TypeMap

type_map: TypeMap = {
    "QueryType": GraphQLObjectType(
        name="QueryType",
        description=None,
        interfaces=[],
        fields=lambda: {
            "_query": GraphQLField(
                GraphQLNonNull(GraphQLString),
                args={},
                description=None,
                deprecation_reason=None,
            )
        },
    ),
    "MutationType": GraphQLObjectType(
        name="MutationType",
        description=None,
        interfaces=[],
        fields=lambda: {
            "_mutation": GraphQLField(
                GraphQLNonNull(GraphQLString),
                args={},
                description=None,
                deprecation_reason=None,
            )
        },
    ),
    "SubscriptionType": GraphQLObjectType(
        name="SubscriptionType",
        description=None,
        interfaces=[],
        fields=lambda: {
            "_subscription": GraphQLField(
                GraphQLNonNull(GraphQLString),
                args={},
                description=None,
                deprecation_reason=None,
            )
        },
    ),
    "InputA": GraphQLInputObjectType(
        name="InputA",
        description=None,
        fields=lambda: {
            "fieldA": GraphQLInputField(
                GraphQLNonNull(GraphQLInt),
                default_value=Undefined,
                description=None,
                deprecation_reason=None,
            )
        },
    ),
    "InterfaceB": GraphQLInterfaceType(
        name="InterfaceB",
        description=None,
        interfaces=[],
        fields=lambda: {
            "id": GraphQLField(
                GraphQLNonNull(GraphQLID),
                args={},
                description=None,
                deprecation_reason=None,
            )
        },
    ),
    "TypeC": GraphQLObjectType(
        name="TypeC",
        description=None,
        interfaces=lambda: cast(list[GraphQLInterfaceType], [type_map["InterfaceB"]]),
        fields=lambda: {
            "id": GraphQLField(
                GraphQLNonNull(GraphQLID),
                args={},
                description=None,
                deprecation_reason=None,
            ),
            "fieldC": GraphQLField(
                GraphQLNonNull(GraphQLFloat),
                args={},
                description=None,
                deprecation_reason=None,
            ),
        },
    ),
    "TypeD": GraphQLObjectType(
        name="TypeD",
        description=None,
        interfaces=[],
        fields=lambda: {
            "fieldD": GraphQLField(
                GraphQLNonNull(GraphQLBoolean),
                args={},
                description=None,
                deprecation_reason=None,
            )
        },
    ),
    "UnionE": GraphQLUnionType(
        name="UnionE",
        description=None,
        types=lambda: cast(
            list[GraphQLObjectType], [type_map["TypeC"], type_map["TypeD"]]
        ),
    ),
    "EnumF": GraphQLEnumType(
        name="EnumF",
        description=None,
        values={
            "F1": GraphQLEnumValue(
                value="F1", description=None, deprecation_reason=None
            ),
            "F2": GraphQLEnumValue(
                value="F2", description=None, deprecation_reason=None
            ),
        },
    ),
    "ScalarG": GraphQLScalarType(
        name="ScalarG", description=None, specified_by_url=None
    ),
}
schema: GraphQLSchema = GraphQLSchema(
    query=cast(GraphQLObjectType, type_map["QueryType"]),
    mutation=cast(GraphQLObjectType, type_map["MutationType"]),
    subscription=cast(GraphQLObjectType, type_map["SubscriptionType"]),
    types=type_map.values(),
    directives=[
        GraphQLDirective(
            name="testDirective",
            description=None,
            is_repeatable=False,
            locations=(DirectiveLocation.FIELD_DEFINITION,),
            args=None,
        ),
        GraphQLDirective(
            name="include",
            description="Directs the executor to include this field or fragment only when the `if` argument is true.",
            is_repeatable=False,
            locations=(
                DirectiveLocation.FIELD,
                DirectiveLocation.FRAGMENT_SPREAD,
                DirectiveLocation.INLINE_FRAGMENT,
            ),
            args={
                "if": GraphQLArgument(
                    GraphQLNonNull(GraphQLBoolean),
                    default_value=Undefined,
                    description="Included when true.",
                    deprecation_reason=None,
                )
            },
        ),
        GraphQLDirective(
            name="skip",
            description="Directs the executor to skip this field or fragment when the `if` argument is true.",
            is_repeatable=False,
            locations=(
                DirectiveLocation.FIELD,
                DirectiveLocation.FRAGMENT_SPREAD,
                DirectiveLocation.INLINE_FRAGMENT,
            ),
            args={
                "if": GraphQLArgument(
                    GraphQLNonNull(GraphQLBoolean),
                    default_value=Undefined,
                    description="Skipped when true.",
                    deprecation_reason=None,
                )
            },
        ),
        GraphQLDirective(
            name="deprecated",
            description="Marks an element of a GraphQL schema as no longer supported.",
            is_repeatable=False,
            locations=(
                DirectiveLocation.FIELD_DEFINITION,
                DirectiveLocation.ARGUMENT_DEFINITION,
                DirectiveLocation.INPUT_FIELD_DEFINITION,
                DirectiveLocation.ENUM_VALUE,
            ),
            args={
                "reason": GraphQLArgument(
                    GraphQLString,
                    default_value="No longer supported",
                    description="Explains why this element was deprecated, usually also including a suggestion for how to access supported similar data. Formatted using the Markdown syntax, as specified by [CommonMark](https://commonmark.org/).",
                    deprecation_reason=None,
                )
            },
        ),
        GraphQLDirective(
            name="specifiedBy",
            description="Exposes a URL that specifies the behavior of this scalar.",
            is_repeatable=False,
            locations=(DirectiveLocation.SCALAR,),
            args={
                "url": GraphQLArgument(
                    GraphQLNonNull(GraphQLString),
                    default_value=Undefined,
                    description="The URL that specifies the behavior of this scalar.",
                    deprecation_reason=None,
                )
            },
        ),
        GraphQLDirective(
            name="oneOf",
            description="Indicates an Input Object is a OneOf Input Object.",
            is_repeatable=False,
            locations=(DirectiveLocation.INPUT_OBJECT,),
            args=None,
        ),
    ],
    description=None,
)
