import ast

import pytest

from ariadne_codegen.client_generators.constants import (
    ANNOTATED,
    BEFORE_VALIDATOR,
    PLAIN_SERIALIZER,
)
from ariadne_codegen.client_generators.scalars import (
    ScalarData,
    generate_input_scalar_annotation,
    generate_result_scalar_annotation,
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


def test_generate_input_scalar_annotation_returns_annotation_only_with_type():
    scalar_data = ScalarData(type_=".custom_types.TypeA", graphql_name="TYPEA")
    expected_annotation = ast.Name(id="TypeA")

    annotation = generate_input_scalar_annotation(scalar_data)

    assert compare_ast(annotation, expected_annotation)


def test_generate_input_scalar_annotation_returns_annotation_with_serialize():
    scalar_data = ScalarData(
        type_=".custom_types.TypeA",
        graphql_name="TYPEA",
        serialize=".custom_types.serialize_type_a",
        parse=".custom_types.parse_type_a",
    )
    expected_annotation = ast.Subscript(
        value=ast.Name(id=ANNOTATED),
        slice=ast.Tuple(
            elts=[
                ast.Name(id="TypeA"),
                ast.Call(
                    func=ast.Name(id=PLAIN_SERIALIZER),
                    args=[ast.Name(id="serialize_type_a")],
                    keywords=[],
                ),
            ]
        ),
    )

    annotation = generate_input_scalar_annotation(scalar_data)

    assert compare_ast(annotation, expected_annotation)


def test_generate_result_scalar_annotation_returns_annotation_only_with_type():
    scalar_data = ScalarData(type_=".custom_types.TypeA", graphql_name="TYPEA")
    expected_annotation = ast.Name(id="TypeA")

    annotation = generate_result_scalar_annotation(scalar_data)

    assert compare_ast(annotation, expected_annotation)


def test_generate_result_scalar_annotation_returns_annotation_with_parse():
    scalar_data = ScalarData(
        type_=".custom_types.TypeA",
        graphql_name="TYPEA",
        serialize=".custom_types.serialize_type_a",
        parse=".custom_types.parse_type_a",
    )
    expected_annotation = ast.Subscript(
        value=ast.Name(id=ANNOTATED),
        slice=ast.Tuple(
            elts=[
                ast.Name(id="TypeA"),
                ast.Call(
                    func=ast.Name(id=BEFORE_VALIDATOR),
                    args=[ast.Name(id="parse_type_a")],
                    keywords=[],
                ),
            ]
        ),
    )

    annotation = generate_result_scalar_annotation(scalar_data)

    assert compare_ast(annotation, expected_annotation)
