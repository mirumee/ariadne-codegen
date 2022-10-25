import ast
from textwrap import dedent

import pytest

from graphql_sdk_gen.generators.utils import ast_to_str


@pytest.mark.parametrize(
    ["ast_object", "expected_result"],
    [
        (
            ast.ImportFrom(module="xyz", names=[ast.alias(name="Xyz")], level=1),
            "from .xyz import Xyz\n",
        ),
        (ast.Import(names=[ast.alias(name="xyz")]), "import xyz\n"),
        (
            ast.ClassDef(
                name="Xyz", bases=[], keywords=[], body=[ast.Pass()], decorator_list=[]
            ),
            "class Xyz:\n    pass\n",
        ),
        (
            ast.Assign(
                targets=[ast.Name(id="__all__")],
                value=ast.List(elts=[ast.Constant(value="Xyz")]),
                lineno=1,
            ),
            '__all__ = ["Xyz"]\n',
        ),
    ],
)
def test_ast_to_str_returns_correct_string_without_removing_imports(
    ast_object, expected_result
):
    assert ast_to_str(ast_object, False) == expected_result


def test_ast_to_str_removes_unused_imports():
    not_used_imported_class = "Xyz"
    module = ast.Module(
        body=[
            ast.ImportFrom(
                module="xyz", names=[ast.alias(name=not_used_imported_class)], level=0
            ),
            ast.ImportFrom(module="efg", names=[ast.alias(name="Efg")], level=0),
            ast.ClassDef(
                name="TestClass",
                bases=[ast.Name(id="Efg")],
                keywords=[],
                body=[ast.Pass()],
                decorator_list=[],
            ),
        ],
        type_ignores=[],
    )
    expected_generated_code = dedent(
        """
        from efg import Efg


        class TestClass(Efg):
            pass
        """
    ).lstrip()

    generated_code = ast_to_str(module, True)

    assert generated_code == expected_generated_code
    assert not_used_imported_class not in generated_code
