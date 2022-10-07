import ast
from typing import Any, Optional, Union

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

from ..exceptions import ParsingError
from .constants import ANY, LIST, OPTIONAL, SIMPLE_TYPE_MAP, UNION


def generate_import_from(
    names: list[str], from_: str, level: int = 0
) -> ast.ImportFrom:
    """Generate import from statement."""
    return ast.ImportFrom(
        module=from_, names=[ast.alias(n) for n in names], level=level
    )


def generate_nullable_annotation(
    slice_: Union[ast.Name, ast.Subscript]
) -> ast.Subscript:
    """Generate optional annotation."""
    return ast.Subscript(value=ast.Name(id=OPTIONAL), slice=slice_)


def generate_annotation_name(
    name, nullable: bool = True
) -> Union[ast.Name, ast.Subscript]:
    """Generate annotation."""
    result = ast.Name(id=name)
    return result if not nullable else generate_nullable_annotation(result)


def generate_list_annotation(
    slice_: Union[ast.Name, ast.Subscript], nullable: bool = True
) -> ast.Subscript:
    """Generate list annotation."""
    result = ast.Subscript(value=ast.Name(id=LIST), slice=slice_)
    return result if not nullable else generate_nullable_annotation(result)


def generate_arg(
    name: str, annotation: Optional[Union[ast.Name, ast.Subscript]] = None
) -> ast.arg:
    """Generate arg."""
    return ast.arg(arg=name, annotation=annotation)


def generate_arguments(args: Optional[list[ast.arg]] = None) -> ast.arguments:
    """Generate arguments."""
    return ast.arguments(
        posonlyargs=[],
        args=args if args else [],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[],
    )


def generate_async_method_definition(
    name: str,
    arguments: ast.arguments,
    return_type: Union[ast.Name, ast.Subscript],
    body: Optional[list[ast.stmt]] = None,
    lineno: int = 1,
) -> ast.AsyncFunctionDef:
    """Generate async function."""
    return ast.AsyncFunctionDef(
        name=name,
        args=arguments,
        body=body if body else [ast.Pass()],
        decorator_list=[],
        returns=return_type,
        lineno=lineno,
    )


def generate_class_def(
    name: str, base_names: Optional[list[str]] = None
) -> ast.ClassDef:
    """Generate class definition."""
    bases = [ast.Name(id=name) for name in base_names] if base_names else []
    return ast.ClassDef(
        name=name,
        bases=bases,
        keywords=[],
        body=[],
        decorator_list=[],
    )


def generate_name(name: str) -> ast.Name:
    """Generate name object."""
    return ast.Name(id=name)


def generate_constant(value: Any) -> ast.Constant:
    """Generate constant object."""
    return ast.Constant(value=value)


def generate_assign(targets: list[str], value: ast.expr, lineno: int = 1) -> ast.Assign:
    """Generate assign object."""
    return ast.Assign(
        targets=[ast.Name(t) for t in targets], value=value, lineno=lineno
    )


def generate_ann_assign(
    target: str, annotation: Union[ast.Name, ast.Subscript], lineno: int = 1
) -> ast.AnnAssign:
    """Generate ann assign object."""
    return ast.AnnAssign(
        target=ast.Name(id=target),
        annotation=annotation,
        simple=1,
        lineno=lineno,
    )


def generate_union_annotation(
    types: list[Union[ast.Name, ast.Subscript]], nullable: bool = True
) -> ast.Subscript:
    """Generate union annotation."""
    result = ast.Subscript(value=ast.Name(id=UNION), slice=ast.Tuple(elts=types))
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
    """Parse graphql type and return generated annotation."""
    if isinstance(type_, GraphQLScalarType):
        return generate_annotation_name(SIMPLE_TYPE_MAP.get(type_.name, ANY), nullable)
    if isinstance(
        type_,
        (
            GraphQLObjectType,
            GraphQLInputObjectType,
            GraphQLEnumType,
            GraphQLInterfaceType,
        ),
    ):
        return generate_annotation_name('"' + type_.name + '"', nullable)
    if isinstance(type_, GraphQLUnionType):
        subtypes = [parse_field_type(subtype) for subtype in type_.types]
        return generate_union_annotation(subtypes, nullable)
    if isinstance(type_, GraphQLList):
        return generate_list_annotation(
            parse_field_type(type_.of_type, nullable), nullable
        )
    if isinstance(type_, GraphQLNonNull):
        return parse_field_type(type_.of_type, False)
    raise ParsingError("Invalid field type.")
