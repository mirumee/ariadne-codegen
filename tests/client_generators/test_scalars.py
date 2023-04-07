import ast

import pytest

from ariadne_codegen.client_generators.constants import (
    ANY,
    CALLABLE,
    DICT,
    SCALARS_PARSE_DICT_NAME,
    SCALARS_SERIALIZE_DICT_NAME,
    TYPING_MODULE,
)
from ariadne_codegen.client_generators.scalars import (
    ScalarData,
    ScalarsDefinitionsGenerator,
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


def test_generate_without_scalars_returns_module_with_empty_dicts():
    expected_module = ast.Module(
        body=[
            ast.ImportFrom(
                module=TYPING_MODULE,
                names=[
                    ast.alias(name=DICT),
                    ast.alias(name=ANY),
                    ast.alias(name=CALLABLE),
                ],
                level=0,
            ),
            ast.AnnAssign(
                target=ast.Name(id=SCALARS_PARSE_DICT_NAME),
                annotation=ast.Subscript(
                    value=ast.Name(id=DICT),
                    slice=ast.Tuple(
                        elts=[
                            ast.Name(id=ANY),
                            ast.Subscript(
                                value=ast.Name(id=CALLABLE),
                                slice=ast.Tuple(
                                    elts=[
                                        ast.List(elts=[ast.Name(id="str")]),
                                        ast.Name(id=ANY),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
                value=ast.Dict(keys=[], values=[]),
                simple=1,
            ),
            ast.AnnAssign(
                target=ast.Name(id=SCALARS_SERIALIZE_DICT_NAME),
                annotation=ast.Subscript(
                    value=ast.Name(id=DICT),
                    slice=ast.Tuple(
                        elts=[
                            ast.Name(id=ANY),
                            ast.Subscript(
                                value=ast.Name(id=CALLABLE),
                                slice=ast.Tuple(
                                    elts=[
                                        ast.List(elts=[ast.Name(id=ANY)]),
                                        ast.Name(id="str"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
                value=ast.Dict(keys=[], values=[]),
                simple=1,
            ),
        ],
        type_ignores=[],
    )

    module = ScalarsDefinitionsGenerator().generate()

    assert compare_ast(module, expected_module)


def test_generate_returns_module_with_dictionaries_with_scalars_methods():
    generator = ScalarsDefinitionsGenerator(
        scalars_data=[
            ScalarData(type_="str"),
            ScalarData(type_="datetime.datetime"),
            ScalarData(
                type_=".scalar_a.ScalarA",
                serialize=".scalar_a.serialize_a",
                parse=".scalar_a.parse_a",
            ),
            ScalarData(
                type_=".scalar_b.ScalarB",
                serialize=".scalar_b.serialize_b",
            ),
            ScalarData(
                type_=".scalar_c.ScalarC",
                parse=".scalar_c.parse_c",
            ),
        ]
    )
    expected_module = ast.Module(
        body=[
            ast.ImportFrom(
                module="typing",
                names=[
                    ast.alias(name="Dict"),
                    ast.alias(name="Any"),
                    ast.alias(name="Callable"),
                ],
                level=0,
            ),
            ast.ImportFrom(
                module=".scalar_a", names=[ast.alias(name="ScalarA")], level=0
            ),
            ast.ImportFrom(
                module=".scalar_a", names=[ast.alias(name="serialize_a")], level=0
            ),
            ast.ImportFrom(
                module=".scalar_a", names=[ast.alias(name="parse_a")], level=0
            ),
            ast.ImportFrom(
                module=".scalar_b", names=[ast.alias(name="ScalarB")], level=0
            ),
            ast.ImportFrom(
                module=".scalar_b", names=[ast.alias(name="serialize_b")], level=0
            ),
            ast.ImportFrom(
                module=".scalar_c", names=[ast.alias(name="ScalarC")], level=0
            ),
            ast.ImportFrom(
                module=".scalar_c", names=[ast.alias(name="parse_c")], level=0
            ),
            ast.AnnAssign(
                target=ast.Name(id=SCALARS_PARSE_DICT_NAME),
                annotation=ast.Subscript(
                    value=ast.Name(id=DICT),
                    slice=ast.Tuple(
                        elts=[
                            ast.Name(id=ANY),
                            ast.Subscript(
                                value=ast.Name(id=CALLABLE),
                                slice=ast.Tuple(
                                    elts=[
                                        ast.List(elts=[ast.Name(id="str")]),
                                        ast.Name(id=ANY),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
                value=ast.Dict(
                    keys=[ast.Name(id="ScalarA"), ast.Name(id="ScalarC")],
                    values=[ast.Name(id="parse_a"), ast.Name(id="parse_c")],
                ),
                simple=1,
            ),
            ast.AnnAssign(
                target=ast.Name(id=SCALARS_SERIALIZE_DICT_NAME),
                annotation=ast.Subscript(
                    value=ast.Name(id=DICT),
                    slice=ast.Tuple(
                        elts=[
                            ast.Name(id=ANY),
                            ast.Subscript(
                                value=ast.Name(id=CALLABLE),
                                slice=ast.Tuple(
                                    elts=[
                                        ast.List(elts=[ast.Name(id=ANY)]),
                                        ast.Name(id="str"),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
                value=ast.Dict(
                    keys=[ast.Name(id="ScalarA"), ast.Name(id="ScalarB")],
                    values=[ast.Name(id="serialize_a"), ast.Name(id="serialize_b")],
                ),
                simple=1,
            ),
        ],
        type_ignores=[],
    )

    module = generator.generate()

    assert compare_ast(module, expected_module)


def test_generate_triggers_generate_scalars_module_hook(mocker):
    mocked_plugin_manager = mocker.MagicMock()

    ScalarsDefinitionsGenerator(plugin_manager=mocked_plugin_manager).generate()

    assert mocked_plugin_manager.generate_scalars_module.called


def test_generate_triggers_generate_scalars_parse_dict_hook(mocker):
    mocked_plugin_manager = mocker.MagicMock()

    ScalarsDefinitionsGenerator(plugin_manager=mocked_plugin_manager).generate()

    assert mocked_plugin_manager.generate_scalars_parse_dict.called


def test_generate_triggers_generate_scalars_serialize_dict_hook(mocker):
    mocked_plugin_manager = mocker.MagicMock()

    ScalarsDefinitionsGenerator(plugin_manager=mocked_plugin_manager).generate()

    assert mocked_plugin_manager.generate_scalars_serialize_dict.called
