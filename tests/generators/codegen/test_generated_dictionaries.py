import ast

from graphql_sdk_gen.generators.codegen import generate_dict


def test_generate_dict_returns_dict_object():
    result = generate_dict([ast.Constant(value="key")], [ast.Constant(value="value")])

    assert isinstance(result, ast.Dict)
    assert len(result.keys) == 1
    key = result.keys[0]
    assert isinstance(key, ast.Constant)
    assert key.value == "key"
    assert len(result.values) == 1
    value = result.values[0]
    assert isinstance(value, ast.Constant)
    assert value.value == "value"


def test_generate_dict_without_arguments_returns_empty_dict_object():
    result = generate_dict()

    assert isinstance(result, ast.Dict)
    assert not result.keys
    assert not result.values
