import ast

from ariadne_codegen.client_generators.constants import OPTIONAL
from ariadne_codegen.codegen import generate_annotation_name, generate_name


def test_generate_name_returns_name_object():
    value = "xyz"

    result = generate_name(value)

    assert isinstance(result, ast.Name)
    assert result.id == value


def test_generate_annotation_name_returns_not_optional_annotation():
    name = "xyz"

    result = generate_annotation_name(name, False)

    assert isinstance(result, ast.Name)
    assert result.id == name


def test_generate_annotation_name_returns_optional_annotation():
    name = "xyz"

    result = generate_annotation_name(name, True)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
    assert isinstance(result.slice, ast.Name)
    assert result.slice.id == name
