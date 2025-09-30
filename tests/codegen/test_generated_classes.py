import ast

from ariadne_codegen.codegen import generate_class_def


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


def test_generate_class_def_with_description_adds_docstring():
    name = "Xyz"
    description = "This is a test class. \nWith multiple lines."

    result = generate_class_def(name, description=description)

    assert isinstance(result, ast.ClassDef)
    assert result.name == name
    docstring = result.body[0]
    assert isinstance(docstring, ast.Expr)
    assert isinstance(docstring.value, ast.Constant)
    assert docstring.value.value == description