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
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLSchema,
    GraphQLString,
    Undefined,
)
from graphql.type.schema import TypeMap

example_type_map: TypeMap = {
    "Query": GraphQLObjectType(
        name="Query",
        description=None,
        interfaces=[],
        fields=lambda: {
            "users": GraphQLField(
                GraphQLNonNull(
                    GraphQLList(
                        GraphQLNonNull(
                            cast(GraphQLObjectType, example_type_map["User"])
                        )
                    )
                ),
                args={
                    "country": GraphQLArgument(
                        GraphQLString,
                        default_value=Undefined,
                        description=None,
                        deprecation_reason=None,
                    )
                },
                description=None,
                deprecation_reason=None,
            )
        },
    ),
    "Mutation": GraphQLObjectType(
        name="Mutation",
        description=None,
        interfaces=[],
        fields=lambda: {
            "userCreate": GraphQLField(
                cast(GraphQLObjectType, example_type_map["User"]),
                args={
                    "userData": GraphQLArgument(
                        GraphQLNonNull(
                            cast(
                                GraphQLInputObjectType,
                                example_type_map["UserCreateInput"],
                            )
                        ),
                        default_value=Undefined,
                        description=None,
                        deprecation_reason=None,
                    )
                },
                description=None,
                deprecation_reason=None,
            ),
            "userPreferences": GraphQLField(
                GraphQLNonNull(GraphQLBoolean),
                args={
                    "data": GraphQLArgument(
                        cast(
                            GraphQLInputObjectType,
                            example_type_map["UserPreferencesInput"],
                        ),
                        default_value=Undefined,
                        description=None,
                        deprecation_reason=None,
                    )
                },
                description=None,
                deprecation_reason=None,
            ),
        },
    ),
    "UserCreateInput": GraphQLInputObjectType(
        name="UserCreateInput",
        description=None,
        fields=lambda: {
            "firstName": GraphQLInputField(
                GraphQLString,
                default_value=Undefined,
                description=None,
                deprecation_reason=None,
            ),
            "lastName": GraphQLInputField(
                GraphQLString,
                default_value=Undefined,
                description=None,
                deprecation_reason=None,
            ),
            "email": GraphQLInputField(
                GraphQLNonNull(GraphQLString),
                default_value=Undefined,
                description=None,
                deprecation_reason=None,
            ),
            "favouriteColor": GraphQLInputField(
                cast(GraphQLEnumType, example_type_map["Color"]),
                default_value=Undefined,
                description=None,
                deprecation_reason=None,
            ),
            "location": GraphQLInputField(
                cast(GraphQLInputObjectType, example_type_map["LocationInput"]),
                default_value=Undefined,
                description=None,
                deprecation_reason=None,
            ),
        },
    ),
    "LocationInput": GraphQLInputObjectType(
        name="LocationInput",
        description=None,
        fields=lambda: {
            "city": GraphQLInputField(
                GraphQLString,
                default_value=Undefined,
                description=None,
                deprecation_reason=None,
            ),
            "country": GraphQLInputField(
                GraphQLString,
                default_value=Undefined,
                description=None,
                deprecation_reason=None,
            ),
        },
    ),
    "User": GraphQLObjectType(
        name="User",
        description=None,
        interfaces=[],
        fields=lambda: {
            "id": GraphQLField(
                GraphQLNonNull(GraphQLID),
                args={},
                description=None,
                deprecation_reason=None,
            ),
            "firstName": GraphQLField(
                GraphQLString, args={}, description=None, deprecation_reason=None
            ),
            "lastName": GraphQLField(
                GraphQLString, args={}, description=None, deprecation_reason=None
            ),
            "email": GraphQLField(
                GraphQLNonNull(GraphQLString),
                args={},
                description=None,
                deprecation_reason=None,
            ),
            "favouriteColor": GraphQLField(
                cast(GraphQLEnumType, example_type_map["Color"]),
                args={},
                description=None,
                deprecation_reason=None,
            ),
            "location": GraphQLField(
                cast(GraphQLObjectType, example_type_map["Location"]),
                args={},
                description=None,
                deprecation_reason=None,
            ),
        },
    ),
    "Location": GraphQLObjectType(
        name="Location",
        description=None,
        interfaces=[],
        fields=lambda: {
            "city": GraphQLField(
                GraphQLString, args={}, description=None, deprecation_reason=None
            ),
            "country": GraphQLField(
                GraphQLString, args={}, description=None, deprecation_reason=None
            ),
        },
    ),
    "Color": GraphQLEnumType(
        name="Color",
        description=None,
        values={
            "BLACK": GraphQLEnumValue(
                value="BLACK", description=None, deprecation_reason=None
            ),
            "WHITE": GraphQLEnumValue(
                value="WHITE", description=None, deprecation_reason=None
            ),
            "RED": GraphQLEnumValue(
                value="RED", description=None, deprecation_reason=None
            ),
            "GREEN": GraphQLEnumValue(
                value="GREEN", description=None, deprecation_reason=None
            ),
            "BLUE": GraphQLEnumValue(
                value="BLUE", description=None, deprecation_reason=None
            ),
            "YELLOW": GraphQLEnumValue(
                value="YELLOW", description=None, deprecation_reason=None
            ),
        },
    ),
    "UserPreferencesInput": GraphQLInputObjectType(
        name="UserPreferencesInput",
        description=None,
        fields=lambda: {
            "luckyNumber": GraphQLInputField(
                GraphQLInt, default_value=7, description=None, deprecation_reason=None
            ),
            "favouriteWord": GraphQLInputField(
                GraphQLString,
                default_value="word",
                description=None,
                deprecation_reason=None,
            ),
            "colorOpacity": GraphQLInputField(
                GraphQLFloat,
                default_value=1.0,
                description=None,
                deprecation_reason=None,
            ),
            "excludedTags": GraphQLInputField(
                GraphQLList(GraphQLNonNull(GraphQLString)),
                default_value=["offtop", "tag123"],
                description=None,
                deprecation_reason=None,
            ),
            "notificationsPreferences": GraphQLInputField(
                GraphQLNonNull(
                    cast(
                        GraphQLInputObjectType,
                        example_type_map["NotificationsPreferencesInput"],
                    )
                ),
                default_value={
                    "receiveMails": True,
                    "receivePushNotifications": True,
                    "receiveSms": False,
                    "title": "Mr",
                },
                description=None,
                deprecation_reason=None,
            ),
        },
    ),
    "NotificationsPreferencesInput": GraphQLInputObjectType(
        name="NotificationsPreferencesInput",
        description=None,
        fields=lambda: {
            "receiveMails": GraphQLInputField(
                GraphQLNonNull(GraphQLBoolean),
                default_value=Undefined,
                description=None,
                deprecation_reason=None,
            ),
            "receivePushNotifications": GraphQLInputField(
                GraphQLNonNull(GraphQLBoolean),
                default_value=Undefined,
                description=None,
                deprecation_reason=None,
            ),
            "receiveSms": GraphQLInputField(
                GraphQLNonNull(GraphQLBoolean),
                default_value=Undefined,
                description=None,
                deprecation_reason=None,
            ),
            "title": GraphQLInputField(
                GraphQLNonNull(GraphQLString),
                default_value=Undefined,
                description=None,
                deprecation_reason=None,
            ),
        },
    ),
}
example_schema: GraphQLSchema = GraphQLSchema(
    query=cast(GraphQLObjectType, example_type_map["Query"]),
    mutation=cast(GraphQLObjectType, example_type_map["Mutation"]),
    subscription=None,
    types=example_type_map.values(),
    directives=[
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
            description="Exposes a URL that specifies the behaviour of this scalar.",
            is_repeatable=False,
            locations=(DirectiveLocation.SCALAR,),
            args={
                "url": GraphQLArgument(
                    GraphQLNonNull(GraphQLString),
                    default_value=Undefined,
                    description="The URL that specifies the behaviour of this scalar.",
                    deprecation_reason=None,
                )
            },
        ),
    ],
    description=None,
)
