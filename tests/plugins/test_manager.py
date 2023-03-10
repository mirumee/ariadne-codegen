import ast
from typing import cast

import pytest
from graphql import (
    GraphQLEnumType,
    GraphQLEnumValueMap,
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLSchema,
    VariableDefinitionNode,
)

from ariadne_codegen.plugins.base import Plugin
from ariadne_codegen.plugins.manager import PluginManager


@pytest.fixture
def mocked_plugin_manager(mocker):
    return PluginManager(
        schema=GraphQLSchema(),
        plugins_types=[mocker.MagicMock(), mocker.MagicMock()],
    )


def test_init_creates_plugins_instances():
    class TestPlugin(Plugin):
        pass

    manager = PluginManager(schema=GraphQLSchema(), plugins_types=[TestPlugin])

    assert len(manager.plugins) == 1
    assert isinstance(manager.plugins[0], TestPlugin)


def test_generate_init_module_calls_plugins_generate_init_module(mocked_plugin_manager):
    mocked_plugin_manager.generate_init_module(ast.Module(body=[]))

    assert mocked_plugin_manager.plugins[0].generate_init_module.called
    assert mocked_plugin_manager.plugins[1].generate_init_module.called


def test_generate_init_import_calls_plugins_generate_init_import(mocked_plugin_manager):
    mocked_plugin_manager.generate_init_import(ast.ImportFrom())

    assert mocked_plugin_manager.plugins[0].generate_init_import.called
    assert mocked_plugin_manager.plugins[1].generate_init_import.called


def test_generate_enum_calls_plugins_generate_enum(mocked_plugin_manager):
    mocked_plugin_manager.generate_enum(
        ast.ClassDef(),
        enum_type=GraphQLEnumType("TestEnum", values=cast(GraphQLEnumValueMap, {})),
    )

    assert mocked_plugin_manager.plugins[0].generate_enum.called
    assert mocked_plugin_manager.plugins[1].generate_enum.called


def test_generate_enums_module_calls_plugins_generate_enums_module(
    mocked_plugin_manager,
):
    mocked_plugin_manager.generate_enums_module(ast.Module())

    assert mocked_plugin_manager.plugins[0].generate_enums_module.called
    assert mocked_plugin_manager.plugins[1].generate_enums_module.called


def test_generate_client_module_calls_plugins_generate_client_module(
    mocked_plugin_manager,
):
    mocked_plugin_manager.generate_client_module(ast.Module())

    assert mocked_plugin_manager.plugins[0].generate_client_module.called
    assert mocked_plugin_manager.plugins[1].generate_client_module.called


def test_generate_gql_function_calls_plugins_generate_gql_function(
    mocked_plugin_manager,
):
    mocked_plugin_manager.generate_gql_function(ast.FunctionDef())

    assert mocked_plugin_manager.plugins[0].generate_gql_function.called
    assert mocked_plugin_manager.plugins[1].generate_gql_function.called


def test_generate_client_class_calls_plugins_generate_client_class(
    mocked_plugin_manager,
):
    mocked_plugin_manager.generate_client_class(ast.ClassDef())

    assert mocked_plugin_manager.plugins[0].generate_client_class.called
    assert mocked_plugin_manager.plugins[1].generate_client_class.called


def test_generate_client_import_calls_plugins_generate_client_import(
    mocked_plugin_manager,
):
    mocked_plugin_manager.generate_client_import(ast.ImportFrom())

    assert mocked_plugin_manager.plugins[0].generate_client_import.called
    assert mocked_plugin_manager.plugins[1].generate_client_import.called


def test_generate_client_method_calls_plugins_generate_client_method(
    mocked_plugin_manager,
):
    mocked_plugin_manager.generate_client_method(ast.AsyncFunctionDef())

    assert mocked_plugin_manager.plugins[0].generate_client_method.called
    assert mocked_plugin_manager.plugins[1].generate_client_method.called


def test_generate_arguments_calls_plugins_generate_arguments(
    mocked_plugin_manager,
):
    mocked_plugin_manager.generate_arguments(
        ast.arguments(), variable_definitions=(VariableDefinitionNode(),)
    )

    assert mocked_plugin_manager.plugins[0].generate_arguments.called
    assert mocked_plugin_manager.plugins[1].generate_arguments.called


def test_generate_arguments_dict_calls_plugins_generate_arguments_dict(
    mocked_plugin_manager,
):
    mocked_plugin_manager.generate_arguments_dict(
        ast.Dict(), variable_definitions=(VariableDefinitionNode(),)
    )

    assert mocked_plugin_manager.plugins[0].generate_arguments_dict.called
    assert mocked_plugin_manager.plugins[1].generate_arguments_dict.called


def test_generate_inputs_module_calls_plugins_generate_inputs_module(
    mocked_plugin_manager,
):
    mocked_plugin_manager.generate_inputs_module(ast.Module())

    assert mocked_plugin_manager.plugins[0].generate_inputs_module.called
    assert mocked_plugin_manager.plugins[1].generate_inputs_module.called


def test_generate_input_class_calls_plugins_generate_input_class(mocked_plugin_manager):
    mocked_plugin_manager.generate_input_class(
        ast.ClassDef(), input_type=GraphQLInputObjectType("TestInput", fields={})
    )

    assert mocked_plugin_manager.plugins[0].generate_input_class.called
    assert mocked_plugin_manager.plugins[1].generate_input_class.called


def test_generate_input_field_calls_plugins_generate_input_field(mocked_plugin_manager):
    mocked_plugin_manager.generate_input_field(
        ast.AnnAssign(),
        input_field=GraphQLInputField(GraphQLInputObjectType("TestInput", fields={})),
        field_name="fieldA",
    )

    assert mocked_plugin_manager.plugins[0].generate_input_field.called
    assert mocked_plugin_manager.plugins[1].generate_input_field.called
