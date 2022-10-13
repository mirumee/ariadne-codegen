import ast

from graphql_sdk_gen.generators.codegen import (
    generate_arg,
    generate_arguments,
    generate_async_method_definition,
)


def test_generate_arg_returns_arg_with_correct_data():
    name = "xyz"
    annotation = ast.Name(id="str")

    result = generate_arg(name, annotation)

    assert isinstance(result, ast.arg)
    assert result.arg == name
    assert result.annotation == annotation


def test_generate_arguments_returns_arguments_with_given_args():
    args = [ast.arg(arg="self")]

    result = generate_arguments(args)

    assert isinstance(result, ast.arguments)
    assert result.args == args


def test_generate_async_method_definition_returns_async_function_definition():
    name = "xyz"
    return_type = ast.Name("Xyz")
    arguments = ast.arguments(
        posonlyargs=[],
        args=[ast.arg(arg="self")],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[],
    )

    result = generate_async_method_definition(name, arguments, return_type)

    assert isinstance(result, ast.AsyncFunctionDef)
    assert result.name == name
    assert result.returns == return_type
    assert result.args == arguments
