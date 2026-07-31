import pytest


@pytest.fixture
def mocked_plugin_manager(mocker):
    def no_effect_method(obj, *_, **__):
        return obj

    manager = mocker.MagicMock()
    manager.generate_init_module.side_effect = no_effect_method
    manager.generate_init_import.side_effect = no_effect_method
    manager.generate_enum.side_effect = no_effect_method
    manager.generate_enums_module.side_effect = no_effect_method
    manager.generate_client_module.side_effect = no_effect_method
    manager.generate_gql_function.side_effect = no_effect_method
    manager.generate_client_class.side_effect = no_effect_method
    manager.generate_client_import.side_effect = no_effect_method
    manager.generate_client_method.side_effect = no_effect_method
    manager.generate_arguments.side_effect = no_effect_method
    manager.generate_arguments_dict.side_effect = no_effect_method
    manager.generate_inputs_module.side_effect = no_effect_method
    manager.generate_input_class.side_effect = no_effect_method
    manager.generate_input_field.side_effect = no_effect_method
    manager.generate_result_types_module.side_effect = no_effect_method
    manager.generate_operation_str.side_effect = no_effect_method
    manager.generate_result_class.side_effect = no_effect_method
    manager.generate_result_field.side_effect = no_effect_method
    manager.generate_client_code.side_effect = no_effect_method
    manager.generate_enums_code.side_effect = no_effect_method
    manager.generate_inputs_code.side_effect = no_effect_method
    manager.generate_result_types_code.side_effect = no_effect_method
    manager.copy_code.side_effect = no_effect_method
    manager.generate_init_code.side_effect = no_effect_method
    manager.process_name.side_effect = no_effect_method
    manager.generate_fragments_module.side_effect = no_effect_method
    manager.process_schema.side_effect = no_effect_method
    manager.get_file_comment.side_effect = no_effect_method
    manager.generate_custom_module.side_effect = no_effect_method
    manager.generate_custom_method.side_effect = no_effect_method
    manager.generate_files.side_effect = no_effect_method
    return manager
