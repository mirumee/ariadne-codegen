import ast

from graphql_sdk_gen.generators.codegen import generate_nullable_annotation
from graphql_sdk_gen.generators.constants import OPTIONAL


def test_generate_nullable_annotation_returns_subscript_with_correct_value():
    slice_ = ast.Name(id="xyz")

    result = generate_nullable_annotation(slice_)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
