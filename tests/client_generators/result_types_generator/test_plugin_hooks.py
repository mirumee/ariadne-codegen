from typing import cast

from graphql import OperationDefinitionNode, build_ast_schema, parse

from ariadne_codegen.client_generators.result_types import ResultTypesGenerator

from .schema import SCHEMA_STR


def test_generate_triggers_generate_result_types_module_hook(mocked_plugin_manager):
    query_str = "query CustomQuery { camelCaseQuery { id } }"
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


def test_get_operation_as_str_triggers_generate_operation_str_hook(
    mocked_plugin_manager,
):
    query_str = "query CustomQuery { camelCaseQuery { id } }"
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


def test_generator_triggers_generate_result_class_hook_for_every_class(
    mocked_plugin_manager,
):
    query_str = "query CustomQuery { camelCaseQuery { id } }"

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


def test_generator_triggers_generate_result_field_hook_for_every_field(
    mocked_plugin_manager,
):
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


def test_generator_triggers_process_name_hook_for_every_field(mocked_plugin_manager):
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

    ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        convert_to_snake_case=False,
        plugin_manager=mocked_plugin_manager,
    )

    assert mocked_plugin_manager.process_name.call_count == 4
    assert {c.args[0] for c in mocked_plugin_manager.process_name.mock_calls} == {
        "camelCaseQuery",
        "id",
        "field1",
        "fielda",
    }


def test_generator_triggers_generate_result_class_hook_for_class_with_empty_body(
    mocked_plugin_manager,
):
    query_str = "query CustomQuery { camelCaseQuery { ...CustomFragment } }"

    ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        plugin_manager=mocked_plugin_manager,
        fragments_definitions={
            "CustomFragment": parse(
                "fragment CustomFragment on CustomType { id }"
            ).definitions[0]
        },
    )

    assert "CustomQueryCamelCaseQuery" in {
        c.args[0].name for c in mocked_plugin_manager.generate_result_class.mock_calls
    }


def test_generator_triggers_generate_result_class_hook_once_for_class(
    mocked_plugin_manager,
):
    query_str = """
    query CustomQuery {
        camelCaseQuery {
            id
            field1 {
                fielda
            }
            field2 {
                fieldb
            }
            field3
            scalarField
        }
    }
    """

    ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        plugin_manager=mocked_plugin_manager,
    )

    called_classes_names = [
        c.args[0].name for c in mocked_plugin_manager.generate_result_class.mock_calls
    ]
    assert len(called_classes_names) == len(set(called_classes_names))
