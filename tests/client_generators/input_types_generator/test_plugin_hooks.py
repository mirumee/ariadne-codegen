from graphql import (
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLSchema,
    build_ast_schema,
    parse,
)

from ariadne_codegen.client_generators.input_types import InputTypesGenerator


def test_generator_triggers_generate_input_class_hook_for_every_input_type(
    mocked_plugin_manager,
):
    schema_str = """
    input TestInputA {
        fieldA: String!
    }

    input TestInputB {
        fieldB: Int!
    }
    """

    InputTypesGenerator(
        schema=build_ast_schema(parse(schema_str)), plugin_manager=mocked_plugin_manager
    )

    assert mocked_plugin_manager.generate_input_class.call_count == 2
    mock_calls = mocked_plugin_manager.generate_input_class.mock_calls
    call0_input_type = mock_calls[0].kwargs["input_type"]
    call1_input_type = mock_calls[1].kwargs["input_type"]
    assert isinstance(call0_input_type, GraphQLInputObjectType)
    assert call0_input_type.name == "TestInputA"
    assert isinstance(call1_input_type, GraphQLInputObjectType)
    assert call1_input_type.name == "TestInputB"


def test_generator_triggers_generate_input_field_hook_for_every_input_field(
    mocked_plugin_manager,
):
    schema_str = """
    input TestInputAB {
        fieldA: String!
        fieldB: String!
    }

    input TestInputC {
        fieldC: Int!
    }
    """

    InputTypesGenerator(
        schema=build_ast_schema(parse(schema_str)), plugin_manager=mocked_plugin_manager
    )

    assert mocked_plugin_manager.generate_input_field.call_count == 3
    mock_calls = mocked_plugin_manager.generate_input_field.mock_calls
    assert isinstance(mock_calls[0].kwargs["input_field"], GraphQLInputField)
    assert mock_calls[0].kwargs["field_name"] == "fieldA"
    assert isinstance(mock_calls[1].kwargs["input_field"], GraphQLInputField)
    assert mock_calls[1].kwargs["field_name"] == "fieldB"
    assert isinstance(mock_calls[2].kwargs["input_field"], GraphQLInputField)
    assert mock_calls[2].kwargs["field_name"] == "fieldC"


def test_generate_triggers_generate_inputs_module_hook(mocked_plugin_manager):
    generator = InputTypesGenerator(
        schema=GraphQLSchema(), plugin_manager=mocked_plugin_manager
    )

    generator.generate()

    assert mocked_plugin_manager.generate_inputs_module.called


def test_generate_triggers_process_name_hook_for_every_field(mocked_plugin_manager):
    schema_str = """
    input TestInputAB {
        fieldA: String!
        fieldB: String!
    }

    input TestInputC {
        fieldC: Int!
    }
    """

    InputTypesGenerator(
        schema=build_ast_schema(parse(schema_str)),
        convert_to_snake_case=False,
        plugin_manager=mocked_plugin_manager,
    )

    assert mocked_plugin_manager.process_name.call_count == 3
    mock_calls = mocked_plugin_manager.process_name.mock_calls
    assert {call.args[0] for call in mock_calls} == {"fieldA", "fieldB", "fieldC"}
