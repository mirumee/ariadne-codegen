import ast

from ariadne_codegen.generators.constants import (
    ANY,
    CALLABLE,
    DICT,
    SCALARS_PARSE_DICT_NAME,
    SCALARS_SERIALIZE_DICT_NAME,
    TYPING_MODULE,
)
from ariadne_codegen.generators.scalars import ScalarData, ScalarsDefinitionsGenerator

from ..utils import compare_ast


def test_generate_without_scalars_returns_module_with_empty_dicts():
    expected_module = ast.Module(
        body=[
            [
                ast.ImportFrom(
                    module=TYPING_MODULE,
                    names=[
                        ast.alias(name=DICT),
                        ast.alias(name=ANY),
                        ast.alias(name=CALLABLE),
                    ],
                    level=0,
                )
            ],
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
            ScalarData(type_="datetime", import_="datetime"),
            ScalarData(
                type_="ScalarA",
                serialize="serialize_a",
                parse="parse_a",
                import_=".scalar_a",
            ),
            ScalarData(
                type_="ScalarB",
                serialize="serialize_b",
                import_=".scalar_b",
            ),
            ScalarData(
                type_="ScalarC",
                parse="parse_c",
                import_=".scalar_c",
            ),
        ]
    )
    expected_module = ast.Module(
        body=[
            [
                ast.ImportFrom(
                    module=TYPING_MODULE,
                    names=[
                        ast.alias(name=DICT),
                        ast.alias(name=ANY),
                        ast.alias(name=CALLABLE),
                    ],
                    level=0,
                ),
                ast.ImportFrom(
                    module=".scalar_a",
                    names=[
                        ast.alias(name="ScalarA"),
                        ast.alias(name="serialize_a"),
                        ast.alias(name="parse_a"),
                    ],
                    level=0,
                ),
                ast.ImportFrom(
                    module=".scalar_b",
                    names=[ast.alias(name="ScalarB"), ast.alias(name="serialize_b")],
                    level=0,
                ),
                ast.ImportFrom(
                    module=".scalar_c",
                    names=[ast.alias(name="ScalarC"), ast.alias(name="parse_c")],
                    level=0,
                ),
            ],
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
