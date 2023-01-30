import ast
from typing import Union

from graphql import (
    GraphQLEnumType,
    GraphQLInputObjectType,
    GraphQLInterfaceType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLUnionType,
)

Annotation = Union[ast.Name, ast.Subscript]
AnnotationSlice = Union[Annotation, ast.Tuple]

CodegenResultFieldType = Union[
    GraphQLEnumType,
    GraphQLInterfaceType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLUnionType,
]

CodegenInputFieldType = Union[
    GraphQLEnumType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLScalarType,
    GraphQLInputObjectType,
]
