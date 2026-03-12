from pathlib import Path

from graphql import build_ast_schema, parse

from ariadne_codegen.client_generators.package import get_package_generator
from ariadne_codegen.client_generators.scalars import ScalarData
from ariadne_codegen.plugins.manager import PluginManager
from ariadne_codegen.settings import ClientSettings, CommentsStrategy


def test_get_package_generator_without_default_settings(tmp_path: Path):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    base_client_file_path = tmp_path / "valid_file.txt"
    base_client_file_path.touch()
    base_client_file_path.write_text("class Class")

    test_schema = build_ast_schema(
        parse(
            """
    schema {
      query: Query
      mutation: Mutation
      subscription: Subscription
    }
    type Query {
      query1(num: Int!): Int!
    }

    type Mutation {
        mutation1(num: Int!): Int!
    }

    type Subscription {
      subscription1(num: Int!): Int!
    }
    """
        )
    )

    settings_without_defaults = ClientSettings(
        schema_path=schema_path.as_posix(),
        remote_schema_url="remote_schema_url",
        remote_schema_headers={"header": "header"},
        remote_schema_verify_ssl=False,
        remote_schema_timeout=5,
        enable_custom_operations=True,
        plugins=["imaplugin"],
        queries_path=schema_path.as_posix(),
        target_package_name="target_package_name",
        target_package_path=tmp_path.as_posix(),
        client_name="client_name",
        client_file_name="client_file_name",
        base_client_name="Class",
        base_client_file_path=base_client_file_path.as_posix(),
        enums_module_name="enums_module_name",
        input_types_module_name="input_types_module_name",
        fragments_module_name="fragments_module_name",
        include_comments=CommentsStrategy.NONE,
        convert_to_snake_case=False,
        include_all_inputs=False,
        include_all_enums=False,
        async_client=False,
        opentelemetry_client=True,
        files_to_include=[schema_path.as_posix()],
        scalars={"scalar1": ScalarData(type_="str", graphql_name="scalar1")},
    )
    package_generator = get_package_generator(
        schema=test_schema,
        fragments=[],
        settings=settings_without_defaults,
        plugin_manager=PluginManager(schema=test_schema),
    )

    # separate out the generated clients
    client_generator = package_generator.client_generator
    input_types_generator = package_generator.input_types_generator
    fragments_generator = package_generator.fragments_generator
    custom_query_generator = package_generator.custom_query_generator
    custom_mutation_generator = package_generator.custom_mutation_generator

    # client generator
    assert {i.module for i in client_generator._imports} == {
        "typing",
        "valid_file",
        "base_model",
        "collections.abc",
    }
    assert (
        client_generator.arguments_generator.convert_to_snake_case
        == settings_without_defaults.convert_to_snake_case
    )
    assert (
        client_generator.arguments_generator.custom_scalars
        == settings_without_defaults.scalars
    )
    assert client_generator.name == settings_without_defaults.client_name
    assert (
        client_generator._class_def.bases[0].id
        == settings_without_defaults.base_client_name
    )
    assert (
        client_generator.enums_module_name
        == settings_without_defaults.enums_module_name
    )
    assert (
        client_generator.input_types_module_name
        == settings_without_defaults.input_types_module_name
    )
    assert client_generator.custom_scalars == settings_without_defaults.scalars
    # input types generator
    assert (
        input_types_generator.enums_module
        == settings_without_defaults.enums_module_name
    )
    assert (
        input_types_generator.convert_to_snake_case
        == settings_without_defaults.convert_to_snake_case
    )
    assert input_types_generator.custom_scalars == settings_without_defaults.scalars
    # fragments generator
    assert (
        fragments_generator.enums_module_name
        == settings_without_defaults.enums_module_name
    )
    assert (
        fragments_generator.convert_to_snake_case
        == settings_without_defaults.convert_to_snake_case
    )
    assert fragments_generator.custom_scalars == settings_without_defaults.scalars
    # custom query generator
    assert (
        custom_query_generator.enums_module_name
        == settings_without_defaults.enums_module_name
    )
    assert custom_query_generator.custom_scalars == settings_without_defaults.scalars
    assert (
        custom_query_generator.convert_to_snake_case
        == settings_without_defaults.convert_to_snake_case
    )
    assert (
        custom_query_generator.arguments_generator.convert_to_snake_case
        == settings_without_defaults.convert_to_snake_case
    )
    assert (
        custom_query_generator.arguments_generator.custom_scalars
        == settings_without_defaults.scalars
    )
    # custom mutation generator
    assert (
        custom_mutation_generator.enums_module_name
        == settings_without_defaults.enums_module_name
    )
    assert custom_mutation_generator.custom_scalars == settings_without_defaults.scalars
    assert (
        custom_mutation_generator.convert_to_snake_case
        == settings_without_defaults.convert_to_snake_case
    )
    assert (
        custom_mutation_generator.arguments_generator.convert_to_snake_case
        == settings_without_defaults.convert_to_snake_case
    )
    assert (
        custom_mutation_generator.arguments_generator.custom_scalars
        == settings_without_defaults.scalars
    )
