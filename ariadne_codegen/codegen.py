import ast
from typing import Any, Dict, List, Optional, Union

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

from .client_generators.constants import (
    ANY,
    FIELD_CLASS,
    LIST,
    OPTIONAL,
    SIMPLE_TYPE_MAP,
    UNION,
)
from .client_generators.types import Annotation, CodegenResultFieldType
from .exceptions import ParsingError


def generate_import_from(
    names: List[str], from_: str, level: int = 0
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


def generate_arguments(
    args: Optional[List[ast.arg]] = None,
    defaults: Optional[List[ast.expr]] = None,
    kwarg: Optional[ast.arg] = None,
) -> ast.arguments:
    """Generate arguments."""
    return ast.arguments(
        posonlyargs=[],
        args=args if args else [],
        kwonlyargs=[],
        kw_defaults=[],
        kwarg=kwarg,
        defaults=defaults or [],
    )


def generate_async_method_definition(
    name: str,
    arguments: ast.arguments,
    return_type: Union[ast.Name, ast.Subscript],
    body: Optional[List[ast.stmt]] = None,
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
    name: str,
    base_names: Optional[List[str]] = None,
    body: Optional[List[ast.stmt]] = None,
) -> ast.ClassDef:
    """Generate class definition."""
    bases = [ast.Name(id=name) for name in base_names] if base_names else []
    return ast.ClassDef(
        name=name,
        bases=bases,
        keywords=[],
        body=body if body else [],
        decorator_list=[],
    )


def generate_name(name: str) -> ast.Name:
    """Generate name object."""
    return ast.Name(id=name)


def generate_constant(value: Any) -> ast.Constant:
    """Generate constant object."""
    return ast.Constant(value=value)


def generate_assign(
    targets: List[str], value: Union[ast.expr, List[ast.expr]], lineno: int = 1
) -> ast.Assign:
    """Generate assign object."""
    return ast.Assign(
        targets=[ast.Name(t) for t in targets], value=value, lineno=lineno
    )


def generate_ann_assign(
    target: Union[str, ast.expr],
    annotation: Annotation,
    value: Optional[ast.expr] = None,
    lineno: int = 1,
) -> ast.AnnAssign:
    """Generate ann assign object."""
    return ast.AnnAssign(
        target=target if isinstance(target, ast.expr) else ast.Name(id=target),
        annotation=annotation,
        simple=1,
        value=value,
        lineno=lineno,
    )


def generate_union_annotation(
    types: List[Union[ast.Name, ast.Subscript]], nullable: bool = True
) -> ast.Subscript:
    """Generate union annotation."""
    result = ast.Subscript(value=ast.Name(id=UNION), slice=ast.Tuple(elts=types))
    return result if not nullable else generate_nullable_annotation(result)


def generate_dict(
    keys: Optional[List[ast.expr]] = None,
    values: Optional[List[Optional[ast.expr]]] = None,
) -> ast.Dict:
    """Generate dict object."""
    return ast.Dict(keys=keys if keys else [], values=values if values else [])


def generate_await(value: ast.expr) -> ast.Await:
    """Generate await object."""
    return ast.Await(value=value)


def generate_call(
    func: ast.expr,
    args: Optional[List[Union[ast.expr, List[ast.expr]]]] = None,
    keywords: Optional[List[ast.keyword]] = None,
) -> ast.Call:
    """Generate call object."""
    return ast.Call(
        func=func, args=args if args else [], keywords=keywords if keywords else []
    )


def generate_attribute(value: ast.expr, attr: str) -> ast.Attribute:
    """Generate attribute object."""
    return ast.Attribute(value=value, attr=attr)


def generate_keyword(value: ast.expr, arg: Optional[str] = None) -> ast.keyword:
    """Generate keyword object."""
    return ast.keyword(arg=arg, value=value)


def generate_return(value: Optional[ast.expr] = None) -> ast.Return:
    """Generate return object."""
    return ast.Return(value=value)


def parse_field_type(
    type_: CodegenResultFieldType,
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
        subtypes = [parse_field_type(subtype, False) for subtype in type_.types]
        return generate_union_annotation(subtypes, nullable)

    if isinstance(type_, GraphQLList):
        return generate_list_annotation(
            parse_field_type(type_.of_type, nullable), nullable
        )

    if isinstance(type_, GraphQLNonNull):
        return parse_field_type(type_.of_type, False)

    raise ParsingError("Invalid field type.")


def generate_method_call(
    object_name: str, method_name: str, args: Optional[List[Optional[ast.expr]]] = None
) -> ast.Call:
    """Generate object`s method call."""
    return ast.Call(
        func=ast.Attribute(value=ast.Name(id=object_name), attr=method_name),
        args=args or [],
        keywords=[],
    )


def generate_expr(value: ast.expr):
    """Generate expression object."""
    return ast.Expr(value=value)


def generate_trivial_lambda(name: str, argument_name: str) -> ast.Assign:
    """Generate lambda that returns given argument, eg. gql = lambda q: q."""
    return ast.Assign(
        targets=[ast.Name(id=name)],
        value=ast.Lambda(
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg=argument_name)],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=ast.Name(id=argument_name),
        ),
    )


def generate_list(elements: List[Optional[ast.expr]]) -> ast.List:
    """Generate list object."""
    return ast.List(elts=elements)


def generate_lambda(body: ast.expr, args: Optional[ast.arguments] = None) -> ast.Lambda:
    """Generate lambda definition."""
    return ast.Lambda(args=args or generate_arguments(), body=body)


def generate_pydantic_field(keywords: Dict[str, ast.expr]) -> ast.Call:
    return generate_call(
        func=generate_name(FIELD_CLASS),
        keywords=[
            generate_keyword(value=value, arg=arg) for arg, value in keywords.items()
        ],
    )


def generate_module(body: List[ast.stmt]) -> ast.Module:
    return ast.Module(body=body, type_ignores=[])


def generate_subscript(value: ast.expr, slice_: ast.expr) -> ast.Subscript:
    return ast.Subscript(value=value, slice=slice_)


def generate_tuple(elts: List[ast.expr]) -> ast.Tuple:
    return ast.Tuple(elts=elts)


def generate_method_definition(
    name: str,
    arguments: ast.arguments,
    return_type: Union[ast.Name, ast.Subscript],
    body: Optional[List[ast.stmt]] = None,
    lineno: int = 1,
) -> ast.FunctionDef:
    return ast.FunctionDef(
        name=name,
        args=arguments,
        body=body if body else [ast.Pass()],
        decorator_list=[],
        returns=return_type,
        lineno=lineno,
    )


def generate_async_for(
    target: ast.expr,
    iter_: ast.expr,
    body: Optional[List[ast.stmt]] = None,
    orelse: Optional[List[ast.stmt]] = None,
    lineno: int = 1,
) -> ast.AsyncFor:
    return ast.AsyncFor(
        target=target,
        iter=iter_,
        body=body or [ast.Pass()],
        orelse=orelse or [],
        lineno=lineno,
    )


def generate_yield(value: Optional[ast.expr] = None) -> ast.Yield:
    return ast.Yield(value=value)


def generate_pass() -> ast.Pass:
    return ast.Pass()
