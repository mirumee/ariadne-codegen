import ast

import pytest

from ariadne_codegen.client_generators.scalars import (
    ScalarData,
    generate_scalar_imports,
)

from ..utils import compare_ast, sorted_imports


@pytest.mark.parametrize(
    "data, expected_imports",
    [
        (ScalarData(type_="Scalar"), []),
        (ScalarData(type_="Scalar", serialize="serialize"), []),
        (ScalarData(type_="Scalar", parse="parse"), []),
        (
            ScalarData(type_="ab.cd.Scalar"),
            [ast.ImportFrom(names=[ast.alias("Scalar")], module="ab.cd", level=0)],
        ),
        (
            ScalarData(type_="ab.cd.Scalar", serialize="xyz.serialize"),
            [
                ast.ImportFrom(names=[ast.alias("Scalar")], module="ab.cd", level=0),
                ast.ImportFrom(names=[ast.alias("serialize")], module="xyz", level=0),
            ],
        ),
        (
            ScalarData(type_="ab.cd.Scalar", parse="xyz.parse"),
            [
                ast.ImportFrom(names=[ast.alias("Scalar")], module="ab.cd", level=0),
                ast.ImportFrom(names=[ast.alias("parse")], module="xyz", level=0),
            ],
        ),
        (
            ScalarData(type_="a.Scalar", serialize="b.serialize", parse="c.parse"),
            [
                ast.ImportFrom(names=[ast.alias("Scalar")], module="a", level=0),
                ast.ImportFrom(names=[ast.alias("serialize")], module="b", level=0),
                ast.ImportFrom(names=[ast.alias("parse")], module="c", level=0),
            ],
        ),
    ],
)
def test_generate_scalar_imports_returns_correct_imports(data, expected_imports):
    assert compare_ast(
        sorted_imports(generate_scalar_imports(data)), sorted_imports(expected_imports)
    )


def test_generate_scalar_imports_for_data_with_import_raises_deprecation_warning():
    data = ScalarData(
        type_="Scalar", serialize="serialize", parse="parse", import_="xyz"
    )
    expected_imports = [
        ast.ImportFrom(
            names=[
                ast.alias(data.type_),
                ast.alias(data.serialize),
                ast.alias(data.parse),
            ],
            module=data.import_,
            level=0,
        )
    ]

    with pytest.deprecated_call():
        assert compare_ast(generate_scalar_imports(data), expected_imports)
