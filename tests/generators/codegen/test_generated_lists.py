import ast

from graphql_sdk_gen.generators.codegen import generate_list_annotation
from graphql_sdk_gen.generators.constants import LIST, OPTIONAL


def test_generate_list_annotation_returns_list_annotation():
    slice_ = ast.Name(id="xyz")

    result = generate_list_annotation(slice_, False)

    assert isinstance(result.value, ast.Name)
    assert result.value.id == LIST
    assert result.slice == slice_


def test_generate_list_annotation_returns_optional_list_annotation():
    slice_ = ast.Name(id="xyz")

    result = generate_list_annotation(slice_, True)

    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
    assert isinstance(result.slice, ast.Subscript)
    assert isinstance(result.slice.value, ast.Name)
    assert result.slice.value.id == LIST
    assert result.slice.slice == slice_
