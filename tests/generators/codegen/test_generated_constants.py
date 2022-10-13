import ast

import pytest

from graphql_sdk_gen.generators.codegen import generate_constant


@pytest.mark.parametrize("value", [1, "a", "xyz", True, None])
def test_generate_constant_returns_object_with_given_value(value):
    result = generate_constant(value)

    assert isinstance(result, ast.Constant)
    assert result.value == value
