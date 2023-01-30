import ast

from ariadne_codegen.generators.codegen import (
    generate_attribute,
    generate_await,
    generate_call,
    generate_keyword,
)


def test_generate_call_returns_call_object():
    result = generate_call(
        func=ast.Name(id="xyz"),
        args=[ast.arg(arg="a")],
        keywords=[ast.keyword(arg="b", value=ast.Constant(value=5))],
    )

    assert isinstance(result, ast.Call)
    assert isinstance(result.func, ast.Name)
    assert result.func.id == "xyz"
    argument = result.args[0]
    assert isinstance(argument, ast.arg)
    assert argument.arg == "a"
    keyword = result.keywords[0]
    assert isinstance(keyword, ast.keyword)
    assert keyword.arg == "b"
    assert isinstance(keyword.value, ast.Constant)
    assert keyword.value.value == 5


def test_generate_call_without_optional_arguments_returns_call_without_arguments():
    result = generate_call(func=ast.Name(id="xyz"))

    assert isinstance(result, ast.Call)
    assert isinstance(result.func, ast.Name)
    assert result.func.id == "xyz"
    assert not result.args
    assert not result.keywords


def test_generate_await_returns_await_object():
    result = generate_await(ast.Call(func=ast.Name(id="test_function")))

    assert isinstance(result, ast.Await)
    assert isinstance(result.value, ast.Call)
    assert isinstance(result.value.func, ast.Name)
    assert result.value.func.id == "test_function"


def test_generate_keyword_returns_keyword_object():
    result = generate_keyword(arg="test_variable", value=ast.Name(id="test value"))

    assert isinstance(result, ast.keyword)
    assert result.arg == "test_variable"
    assert isinstance(result.value, ast.Name)
    assert result.value.id == "test value"


def test_generate_attribute_returns_attribute_object():
    result = generate_attribute(ast.Name(id="object"), "method")

    assert isinstance(result, ast.Attribute)
    assert result.attr == "method"
    assert isinstance(result.value, ast.Name)
    assert result.value.id == "object"
