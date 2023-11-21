import ast

import pytest

from ariadne_codegen.contrib.no_reimports import NoReimportsPlugin


@pytest.mark.parametrize(
    "module",
    [
        ast.Module(
            body=[
                ast.ImportFrom(
                    module="input_types", names=[ast.alias(name="InputA")], level=1
                ),
                ast.Assign(
                    targets=[ast.Name(id="__all__")],
                    value=ast.List(elts=[ast.Constant(value="InputA")]),
                ),
            ],
            type_ignores=[],
        ),
        ast.Module(body=[], type_ignores=[]),
    ],
)
def test_generate_init_module_returns_module_without_body(module):
    plugin = NoReimportsPlugin(schema=None, config_dict={})

    modified_module = plugin.generate_init_module(module)

    assert isinstance(modified_module, ast.Module)
    assert not modified_module.body
