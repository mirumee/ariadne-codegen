from typing import cast

from graphql import OperationDefinitionNode, build_ast_schema, parse

from ariadne_codegen.generators.result_types import ResultTypesGenerator

from .schema import SCHEMA_STR


def test_generate_triggers_generate_result_types_module_hook(mocker):
    query_str = "query CustomQuery { camelCaseQuery { id } }"
    mocked_plugin_manager = mocker.MagicMock()
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        plugin_manager=mocked_plugin_manager,
    )

    generator.generate()

    assert mocked_plugin_manager.generate_result_types_module.called


def test_get_operation_as_str_triggers_generate_operation_str_hook(mocker):
    query_str = "query CustomQuery { camelCaseQuery { id } }"
    mocked_plugin_manager = mocker.MagicMock()
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        plugin_manager=mocked_plugin_manager,
    )

    generator.get_operation_as_str()

    assert mocked_plugin_manager.generate_operation_str.called


def test_generator_triggers_generate_result_class_hook_for_every_class(mocker):
    query_str = "query CustomQuery { camelCaseQuery { id } }"
    mocked_plugin_manager = mocker.MagicMock()

    ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        plugin_manager=mocked_plugin_manager,
    )

    assert mocked_plugin_manager.generate_result_class.call_count == 2
    assert {
        c.args[0].name for c in mocked_plugin_manager.generate_result_class.mock_calls
    } == {"CustomQuery", "CustomQueryCamelCaseQuery"}


def test_generator_triggers_generate_result_field_hook_for_every_field(mocker):
    query_str = """
    query CustomQuery {
        camelCaseQuery {
            id
            field1 {
                fielda
            }
        }
    }
    """
    mocked_plugin_manager = mocker.MagicMock()

    ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        plugin_manager=mocked_plugin_manager,
    )

    assert mocked_plugin_manager.generate_result_field.call_count == 4
    assert {
        c.kwargs["field"].name.value
        for c in mocked_plugin_manager.generate_result_field.mock_calls
    } == {"camelCaseQuery", "id", "field1", "fielda"}
