import pytest


@pytest.fixture
def mocked_plugin_manager(mocker):
    def no_effect_method(obj, *_, **__):
        return obj

    manager = mocker.MagicMock()
    manager.generate_client_code.side_effect = no_effect_method
    manager.generate_enums_code.side_effect = no_effect_method
    manager.generate_inputs_code.side_effect = no_effect_method
    manager.generate_result_class.side_effect = no_effect_method
    manager.generate_result_types_code.side_effect = no_effect_method
    manager.copy_code.side_effect = no_effect_method
    manager.generate_scalars_code.side_effect = no_effect_method
    manager.generate_init_code.side_effect = no_effect_method
    manager.process_name.side_effect = no_effect_method
    manager.generate_fragments_module.side_effect = no_effect_method
    manager.generate_scalars_module.side_effect = no_effect_method
    manager.generate_scalar_imports.side_effect = no_effect_method
    return manager
