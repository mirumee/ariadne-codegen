import ast
from typing import cast

import pytest
from graphql import (
    FieldNode,
    GraphQLEnumType,
    GraphQLEnumValueMap,
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLSchema,
    OperationDefinitionNode,
    SelectionSetNode,
    VariableDefinitionNode,
)

from ariadne_codegen.plugins.base import Plugin
from ariadne_codegen.plugins.manager import PluginManager


@pytest.fixture
def plugin_manager_with_mocked_plugins(mocker) -> PluginManager:
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


def test_generate_init_module_calls_plugins_generate_init_module(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_init_module(ast.Module(body=[]))

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_init_module.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_init_module.called


def test_generate_init_import_calls_plugins_generate_init_import(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_init_import(ast.ImportFrom())

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_init_import.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_init_import.called


def test_generate_enum_calls_plugins_generate_enum(plugin_manager_with_mocked_plugins):
    plugin_manager_with_mocked_plugins.generate_enum(
        ast.ClassDef(),
        enum_type=GraphQLEnumType("TestEnum", values=cast(GraphQLEnumValueMap, {})),
    )

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_enum.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_enum.called


def test_generate_enums_module_calls_plugins_generate_enums_module(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_enums_module(ast.Module())

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_enums_module.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_enums_module.called


def test_generate_client_module_calls_plugins_generate_client_module(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_client_module(ast.Module())

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_client_module.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_client_module.called


def test_generate_gql_function_calls_plugins_generate_gql_function(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_gql_function(ast.FunctionDef())

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_gql_function.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_gql_function.called


def test_generate_client_class_calls_plugins_generate_client_class(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_client_class(ast.ClassDef())

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_client_class.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_client_class.called


def test_generate_client_import_calls_plugins_generate_client_import(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_client_import(ast.ImportFrom())

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_client_import.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_client_import.called


def test_generate_client_method_calls_plugins_generate_client_method(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_client_method(
        ast.AsyncFunctionDef(), operation_definition=OperationDefinitionNode()
    )

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_client_method.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_client_method.called


def test_generate_arguments_calls_plugins_generate_arguments(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_arguments(
        ast.arguments(), variable_definitions=(VariableDefinitionNode(),)
    )

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_arguments.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_arguments.called


def test_generate_arguments_dict_calls_plugins_generate_arguments_dict(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_arguments_dict(
        ast.Dict(), variable_definitions=(VariableDefinitionNode(),)
    )

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_arguments_dict.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_arguments_dict.called


def test_generate_inputs_module_calls_plugins_generate_inputs_module(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_inputs_module(ast.Module())

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_inputs_module.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_inputs_module.called


def test_generate_input_class_calls_plugins_generate_input_class(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_input_class(
        ast.ClassDef(), input_type=GraphQLInputObjectType("TestInput", fields={})
    )

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_input_class.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_input_class.called


def test_generate_input_field_calls_plugins_generate_input_field(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_input_field(
        ast.AnnAssign(),
        input_field=GraphQLInputField(GraphQLInputObjectType("TestInput", fields={})),
        field_name="fieldA",
    )

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_input_field.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_input_field.called


def test_generate_result_types_module_calls_plugins_generate_result_types_module(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_result_types_module(
        ast.Module(), operation_definition=OperationDefinitionNode()
    )

    assert plugin_manager_with_mocked_plugins.plugins[
        0
    ].generate_result_types_module.called
    assert plugin_manager_with_mocked_plugins.plugins[
        1
    ].generate_result_types_module.called


def test_generate_operation_str_calls_plugins_generate_operation_str(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_operation_str(
        "", operation_definition=OperationDefinitionNode()
    )

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_operation_str.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_operation_str.called


def test_generate_result_class_calls_plugins_generate_result_class(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_result_class(
        ast.ClassDef(),
        operation_definition=OperationDefinitionNode(),
        selection_set=SelectionSetNode(),
    )

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_result_class.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_result_class.called


def test_generate_result_field_calls_plugins_generate_result_field(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_result_field(
        ast.AnnAssign(),
        operation_definition=OperationDefinitionNode(),
        field=FieldNode(),
    )

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_result_field.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_result_field.called


def test_generate_client_code_calls_plugins_generate_client_code(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_client_code("")

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_client_code.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_client_code.called


def test_generate_enums_code_calls_plugins_generate_enums_code(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_enums_code("")

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_enums_code.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_enums_code.called


def test_generate_inputs_code_calls_plugins_generate_inputs_code(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_inputs_code("")

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_inputs_code.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_inputs_code.called


def test_generate_result_types_code_calls_plugins_generate_result_types_code(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_result_types_code("")

    assert plugin_manager_with_mocked_plugins.plugins[
        0
    ].generate_result_types_code.called
    assert plugin_manager_with_mocked_plugins.plugins[
        1
    ].generate_result_types_code.called


def test_copy_code_calls_plugins_copy_code(plugin_manager_with_mocked_plugins):
    plugin_manager_with_mocked_plugins.copy_code("")

    assert plugin_manager_with_mocked_plugins.plugins[0].copy_code.called
    assert plugin_manager_with_mocked_plugins.plugins[1].copy_code.called


def test_generate_init_code_calls_plugins_generate_init_code(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_init_code("")

    assert plugin_manager_with_mocked_plugins.plugins[0].generate_init_code.called
    assert plugin_manager_with_mocked_plugins.plugins[1].generate_init_code.called


def test_process_name_calls_plugins_process_name(plugin_manager_with_mocked_plugins):
    plugin_manager_with_mocked_plugins.process_name("", OperationDefinitionNode())

    assert plugin_manager_with_mocked_plugins.plugins[0].process_name.called
    assert plugin_manager_with_mocked_plugins.plugins[1].process_name.called


def test_generate_fragments_module_calls_plugins_generate_fragments_module(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.generate_fragments_module(
        ast.Module(body=[]), {}
    )

    plugin1, plugin2 = plugin_manager_with_mocked_plugins.plugins
    assert plugin1.generate_fragments_module.called
    assert plugin2.generate_fragments_module.called


def test_process_schema_calls_plugins_process_schema(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.process_schema(GraphQLSchema())

    plugin1, plugin2 = plugin_manager_with_mocked_plugins.plugins
    assert plugin1.process_schema.called
    assert plugin2.process_schema.called


def test_process_schema_updates_plugins_schema_field():
    class SchemaPugin(Plugin):
        def process_schema(self, schema: GraphQLSchema) -> GraphQLSchema:
            return GraphQLSchema()

    class DumbPlugin(Plugin):
        pass

    org_schema = GraphQLSchema()
    manager = PluginManager(
        schema=org_schema,
        plugins_types=[DumbPlugin, SchemaPugin, DumbPlugin],
    )

    dumb_plugin1, schema_plugin, dump_plugin2 = manager.plugins
    assert dumb_plugin1.schema is org_schema
    assert dump_plugin2.schema is org_schema
    assert schema_plugin.schema is org_schema

    manager.process_schema(org_schema)

    assert dumb_plugin1.schema is not org_schema
    assert dump_plugin2.schema is not org_schema
    assert schema_plugin.schema is not org_schema


def test_get_file_comment_calls_plugins_get_file_comment(
    plugin_manager_with_mocked_plugins,
):
    plugin_manager_with_mocked_plugins.get_file_comment(
        "comment", code="class Xyz:\n    pass", source="queries.graphql"
    )

    plugin1, plugin2 = plugin_manager_with_mocked_plugins.plugins
    assert plugin1.get_file_comment.called
    assert plugin2.get_file_comment.called
