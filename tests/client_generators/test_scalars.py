import ast

import pytest

from ariadne_codegen.client_generators.constants import (
    ANNOTATED,
    BEFORE_VALIDATOR,
    PLAIN_SERIALIZER,
    PYDANTIC_MODULE,
    TYPING_MODULE,
)
from ariadne_codegen.client_generators.scalars import (
    ScalarData,
    ScalarsDefinitionsGenerator,
    generate_scalar_imports,
)

from ..utils import compare_ast, filter_ast_objects, sorted_imports


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


def test_generate_without_scalars_returns_module_with_only_imports():
    expected_imports = [
        ast.ImportFrom(names=[ast.alias(ANNOTATED)], module=TYPING_MODULE, level=0),
        ast.ImportFrom(
            names=[ast.alias(PLAIN_SERIALIZER), ast.alias(BEFORE_VALIDATOR)],
            module=PYDANTIC_MODULE,
            level=0,
        ),
    ]

    module = ScalarsDefinitionsGenerator().generate()

    assert compare_ast(module.body, expected_imports)


def test_generate_return_module_with_annotation_type_for_every_scalar():
    generator = ScalarsDefinitionsGenerator(
        scalars_data=[
            ScalarData(type_="str", graphql_name="ScalarSTR"),
            ScalarData(type_="datetime.datetime", graphql_name="ScalarDatetime"),
            ScalarData(
                type_=".scalar_a.ScalarA",
                serialize=".scalar_a.serialize_a",
                parse=".scalar_a.parse_a",
                graphql_name="ScalarA",
            ),
            ScalarData(
                type_=".scalar_b.ScalarB",
                serialize=".scalar_b.serialize_b",
                graphql_name="ScalarB",
            ),
            ScalarData(
                type_=".scalar_c.ScalarC",
                parse=".scalar_c.parse_c",
                graphql_name="ScalarC",
            ),
        ]
    )

    module = generator.generate()

    types_names = [
        stmt.targets[0].id for stmt in module.body if isinstance(stmt, ast.Assign)
    ]
    assert types_names == [
        "ScalarSTR",
        "ScalarDatetime",
        "ScalarA_",
        "ScalarB_",
        "ScalarC_",
    ]


@pytest.mark.parametrize(
    "scalar_data, expected_assign",
    [
        (
            ScalarData(type_="str", graphql_name="ScalarA"),
            ast.Assign(targets=[ast.Name(id="ScalarA")], value=ast.Name(id="str")),
        ),
        (
            ScalarData(type_="SameName", graphql_name="SameName"),
            ast.Assign(
                targets=[ast.Name(id="SameName_")], value=ast.Name(id="SameName")
            ),
        ),
        (
            ScalarData(type_="TypeA", serialize="serialize_a", graphql_name="ScalarA"),
            ast.Assign(
                targets=[ast.Name(id="ScalarA")],
                value=ast.Subscript(
                    value=ast.Name(id=ANNOTATED),
                    slice=ast.Tuple(
                        elts=[
                            ast.Name("TypeA"),
                            ast.Call(
                                func=ast.Name(id=PLAIN_SERIALIZER),
                                args=[ast.Name(id="serialize_a")],
                                keywords=[],
                            ),
                        ]
                    ),
                ),
            ),
        ),
        (
            ScalarData(type_="TypeA", parse="parse_a", graphql_name="ScalarA"),
            ast.Assign(
                targets=[ast.Name(id="ScalarA")],
                value=ast.Subscript(
                    value=ast.Name(id=ANNOTATED),
                    slice=ast.Tuple(
                        elts=[
                            ast.Name("TypeA"),
                            ast.Call(
                                func=ast.Name(id=BEFORE_VALIDATOR),
                                args=[ast.Name(id="parse_a")],
                                keywords=[],
                            ),
                        ]
                    ),
                ),
            ),
        ),
        (
            ScalarData(
                type_="TypeA",
                serialize="serialize_a",
                parse="parse_a",
                graphql_name="ScalarA",
            ),
            ast.Assign(
                targets=[ast.Name(id="ScalarA")],
                value=ast.Subscript(
                    value=ast.Name(id=ANNOTATED),
                    slice=ast.Tuple(
                        elts=[
                            ast.Name("TypeA"),
                            ast.Call(
                                func=ast.Name(id=PLAIN_SERIALIZER),
                                args=[ast.Name(id="serialize_a")],
                                keywords=[],
                            ),
                            ast.Call(
                                func=ast.Name(id=BEFORE_VALIDATOR),
                                args=[ast.Name(id="parse_a")],
                                keywords=[],
                            ),
                        ]
                    ),
                ),
            ),
        ),
    ],
)
def test_generate_returns_module_with_correct_type_annotation(
    scalar_data, expected_assign
):
    generator = ScalarsDefinitionsGenerator(scalars_data=[scalar_data])

    module = generator.generate()

    generated_assigns = filter_ast_objects(module, ast.Assign)
    assert len(generated_assigns) == 1
    generated_assign = generated_assigns[0]
    assert compare_ast(generated_assign, expected_assign)


def test_generate_triggers_generate_scalars_module_plugin_hook(mocked_plugin_manager):
    generator = ScalarsDefinitionsGenerator(
        scalars_data=[ScalarData(type_="str", graphql_name="ScalarSTR")],
        plugin_manager=mocked_plugin_manager,
    )

    generator.generate()

    assert mocked_plugin_manager.generate_scalars_module.called


def test_generate_triggers_generate_scalar_annotation_plugin_hook_for_every_scalar(
    mocked_plugin_manager,
):
    generator = ScalarsDefinitionsGenerator(
        scalars_data=[
            ScalarData(type_="str", graphql_name="ScalarA"),
            ScalarData(type_="str", graphql_name="ScalarB"),
        ],
        plugin_manager=mocked_plugin_manager,
    )

    generator.generate()

    assert mocked_plugin_manager.generate_scalar_annotation.call_count == 2
    assert [
        c.kwargs["scalar_name"]
        for c in mocked_plugin_manager.generate_scalar_annotation.mock_calls
    ] == ["ScalarA", "ScalarB"]


def test_generate_triggers_generate_scalar_imports_plugin_hook_for_every_scalar(
    mocked_plugin_manager,
):
    generator = ScalarsDefinitionsGenerator(
        scalars_data=[
            ScalarData(type_="str", graphql_name="ScalarA"),
            ScalarData(type_="str", graphql_name="ScalarB"),
        ],
        plugin_manager=mocked_plugin_manager,
    )

    generator.generate()

    assert mocked_plugin_manager.generate_scalar_imports.call_count == 2
    assert [
        c.kwargs["scalar_name"]
        for c in mocked_plugin_manager.generate_scalar_imports.mock_calls
    ] == ["ScalarA", "ScalarB"]
