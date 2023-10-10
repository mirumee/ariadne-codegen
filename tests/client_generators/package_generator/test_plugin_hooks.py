from graphql import parse

from ariadne_codegen.client_generators.arguments import ArgumentsGenerator
from ariadne_codegen.client_generators.client import ClientGenerator
from ariadne_codegen.client_generators.enums import EnumsGenerator
from ariadne_codegen.client_generators.fragments import FragmentsGenerator
from ariadne_codegen.client_generators.init_file import InitFileGenerator
from ariadne_codegen.client_generators.input_types import InputTypesGenerator
from ariadne_codegen.client_generators.package import PackageGenerator


def test_generate_triggers_generate_client_code_hook(
    tmp_path,
    schema,
    async_base_client_import,
    mocked_plugin_manager,
):
    PackageGenerator(
        package_name="test_graphql_client",
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        plugin_manager=mocked_plugin_manager,
    ).generate()

    assert mocked_plugin_manager.generate_client_code.called


def test_generate_triggers_generate_enums_code_hook(
    tmp_path, schema, async_base_client_import, mocked_plugin_manager
):
    PackageGenerator(
        package_name="test_graphql_client",
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        plugin_manager=mocked_plugin_manager,
    ).generate()

    assert mocked_plugin_manager.generate_enums_code.called


def test_generate_triggers_generate_inputs_code_hook(
    tmp_path, schema, async_base_client_import, mocked_plugin_manager
):
    PackageGenerator(
        package_name="test_graphql_client",
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        plugin_manager=mocked_plugin_manager,
    ).generate()

    assert mocked_plugin_manager.generate_inputs_code.called


def test_generate_triggers_generate_result_types_code_hook_for_every_added_operation(
    tmp_path, schema, async_base_client_import, mocked_plugin_manager
):
    generator = PackageGenerator(
        package_name="test_graphql_client",
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        plugin_manager=mocked_plugin_manager,
    )
    generator.add_operation(parse("query A { query2 { id } }").definitions[0])
    generator.add_operation(parse("query B { query2 { id } }").definitions[0])

    generator.generate()

    assert mocked_plugin_manager.generate_result_types_code.call_count == 2


def test_generate_triggers_copy_code_hook_for_every_attached_dependency_file(
    tmp_path, schema, async_base_client_import, mocked_plugin_manager
):
    PackageGenerator(
        package_name="test_graphql_client",
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        plugin_manager=mocked_plugin_manager,
    ).generate()

    assert mocked_plugin_manager.copy_code.call_count == 3


def test_generate_triggers_copy_code_hook_for_every_file_to_include(
    tmp_path, schema, async_base_client_import, mocked_plugin_manager
):
    test_file_path = tmp_path / "xyz.py"
    test_file_path.touch()

    PackageGenerator(
        package_name="test_graphql_client",
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        plugin_manager=mocked_plugin_manager,
        files_to_include=[test_file_path.as_posix()],
    ).generate()

    assert mocked_plugin_manager.copy_code.call_count == 4


def test_generate_triggers_generate_init_code_hook(
    tmp_path, schema, async_base_client_import, mocked_plugin_manager
):
    PackageGenerator(
        package_name="test_graphql_client",
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        plugin_manager=mocked_plugin_manager,
    ).generate()

    assert mocked_plugin_manager.generate_init_code.called


def test_add_operation_triggers_process_name_hook(
    tmp_path, schema, async_base_client_import, mocked_plugin_manager
):
    query_str = """
    query custom_query_name {
        query2 {
            id
        }
    }
    """

    PackageGenerator(
        package_name="test_graphql_client",
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        plugin_manager=mocked_plugin_manager,
    ).add_operation(parse(query_str).definitions[0])

    assert mocked_plugin_manager.process_name.called
    assert "custom_query_name" in {
        c.args[0] for c in mocked_plugin_manager.process_name.mock_calls
    }
