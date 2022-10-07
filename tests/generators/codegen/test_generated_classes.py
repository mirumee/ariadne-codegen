import ast

from graphql_sdk_gen.generators.codegen import generate_class_def


def test_generate_class_def_returns_class_def_with_correct_bases():
    name = "Xyz"
    base_name = "BaseClass"

    result = generate_class_def(name, [base_name])

    assert isinstance(result, ast.ClassDef)
    assert result.name == name
    base = result.bases[0]
    assert isinstance(base, ast.Name)
    assert base.id == base_name


def test_generate_class_def_returns_class_def_without_base():
    name = "Xyz"

    result = generate_class_def(name)

    assert isinstance(result, ast.ClassDef)
    assert result.name == name
    assert not result.bases
