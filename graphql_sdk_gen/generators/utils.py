import ast
from typing import Union, Optional

import isort
from black import Mode, format_str
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
from .constants import LIST, OPTIONAL, SIMPLE_TYPE_MAP


def ast_to_str(ast_obj: ast.AST) -> str:
    """Convert ast object into string."""
    return format_str(isort.code(ast.unparse(ast_obj)), mode=Mode())


def generate_import_from(
    names: list[str], from_: str, level: int = 0
) -> ast.ImportFrom:
    """Generate import from statement."""
    return ast.ImportFrom(
        module=from_, names=[ast.alias(n) for n in names], level=level
    )


def to_snake_case(name: str) -> str:
    result = "".join([f"_{c.lower()}" if c.isupper() else c for c in name])
    return result[1:] if result.startswith("_") else result


def generate_class_def(name: str, base_names: Optional[list[str]] = None):
    bases = [ast.Name(id=name) for name in base_names] if base_names else []
    return ast.ClassDef(
        name=name,
        bases=bases,
        keywords=[],
        body=[],
        decorator_list=[],
    )


def generate_nullable_annotation(
    slice_: Union[ast.Name, ast.Subscript]
) -> ast.Subscript:
    return ast.Subscript(value=ast.Name(id=OPTIONAL), slice=slice_)


def generate_annotation_name(
    name, nullable: bool = True
) -> Union[ast.Name, ast.Subscript]:
    result = ast.Name(id=name)
    return result if not nullable else generate_nullable_annotation(result)


def generate_list_annotation(
    slice_: Union[ast.Name, ast.Subscript], nullable: bool = True
):
    result = ast.Subscript(value=ast.Name(id=LIST), slice=slice_)
    return result if not nullable else generate_nullable_annotation(result)


def generate_union_annotation(
    types: list[Union[ast.Name, ast.Subscript]], nullable: bool = True
) -> ast.Subscript:
    result = ast.Subscript(value=ast.Name(id="Union"), slice=ast.Tuple(elts=types))
    return result if not nullable else generate_nullable_annotation(result)


def parse_field_type(
    type_: Union[
        GraphQLEnumType,
        GraphQLInputObjectType,
        GraphQLInterfaceType,
        GraphQLList,
        GraphQLNonNull,
        GraphQLObjectType,
        GraphQLScalarType,
        GraphQLUnionType,
    ],
    nullable: bool = True,
) -> Union[ast.Name, ast.Subscript]:
    if isinstance(type_, GraphQLScalarType):
        return generate_annotation_name(
            SIMPLE_TYPE_MAP.get(type_.name, "Any"), nullable
        )
    elif isinstance(
        type_,
        (
            GraphQLObjectType,
            GraphQLInputObjectType,
            GraphQLEnumType,
            GraphQLInterfaceType,
        ),
    ):
        return generate_annotation_name(type_.name, nullable)
    elif isinstance(type_, GraphQLUnionType):
        subtypes = [parse_field_type(subtype) for subtype in type_.types]
        return generate_union_annotation(subtypes, nullable)
    elif isinstance(type_, GraphQLList):
        return generate_list_annotation(
            parse_field_type(type_.of_type, nullable), nullable
        )
    elif isinstance(type_, GraphQLNonNull):
        return parse_field_type(type_.of_type, False)
    else:
        raise Exception


def walk_annotation(annotation):
    if isinstance(annotation, ast.Name):
        return annotation.id
    return walk_annotation(annotation.slice)


def add_prefix_to_annotation(annotation, prefix):
    if isinstance(annotation, ast.Name):
        return ast.Name(id=prefix + annotation.id)
    elif isinstance(annotation, ast.Subscript):
        return ast.Subscript(
            value=annotation.value,
            slice=add_prefix_to_annotation(annotation.slice, prefix),
        )
