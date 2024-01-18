import os
from pathlib import Path
from textwrap import dedent

import pytest

from ariadne_codegen.client_generators.dependencies import (
    async_base_client,
    async_base_client_open_telemetry,
    base_client,
    base_client_open_telemetry,
)
from ariadne_codegen.config import ClientSettings, GraphQLSchemaSettings
from ariadne_codegen.exceptions import InvalidConfiguration


def test_client_settings_instance_is_created_with_base_client_defined_in_file(tmp_path):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    base_client_file_content = """
    class BaseClient:
        pass
    """
    base_client_file_path = tmp_path / "base_client.py"
    base_client_file_path.write_text(dedent(base_client_file_content))

    ClientSettings(
        schema_path=schema_path.as_posix(),
        queries_path=queries_path.as_posix(),
        base_client_name="BaseClient",
        base_client_file_path=base_client_file_path.as_posix(),
    )


def test_client_settings_with_invalid_base_client_file_raises_invalid_configuration(
    tmp_path,
):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    base_client_file_path = tmp_path / "invalid_file.txt"
    base_client_file_path.write_text("invalid content")

    with pytest.raises(InvalidConfiguration):
        ClientSettings(
            schema_path=schema_path.as_posix(),
            queries_path=queries_path.as_posix(),
            base_client_file_path=base_client_file_path.as_posix(),
            base_client_name="BaseClient",
        )


def test_client_settings_with_invalid_base_client_name_raises_configuration_exception(
    tmp_path,
):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    base_client_file_content = """
    class BaseClient:
        pass
    """
    base_client_file_path = tmp_path / "base_client.py"
    base_client_file_path.write_text(dedent(base_client_file_content))

    with pytest.raises(InvalidConfiguration):
        ClientSettings(
            schema_path=schema_path.as_posix(),
            queries_path=queries_path.as_posix(),
            base_client_name="OtherClient",
            base_client_file_path=base_client_file_path.as_posix(),
        )


@pytest.mark.parametrize(
    "async_client, opentelemetry_client, expected_name, expected_path",
    [
        (
            True,
            True,
            "AsyncBaseClientOpenTelemetry",
            async_base_client_open_telemetry.__file__,
        ),
        (True, False, "AsyncBaseClient", async_base_client.__file__),
        (False, True, "BaseClientOpenTelemetry", base_client_open_telemetry.__file__),
        (False, False, "BaseClient", base_client.__file__),
    ],
)
def test_client_settings_sets_correct_default_values_for_base_client_name_and_path(
    tmp_path, async_client, opentelemetry_client, expected_name, expected_path
):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    settings = ClientSettings(
        schema_path=schema_path,
        queries_path=queries_path,
        async_client=async_client,
        opentelemetry_client=opentelemetry_client,
    )

    assert settings.base_client_name == expected_name
    assert settings.base_client_file_path == Path(expected_path).as_posix()


def test_client_settings_without_schema_path_with_remote_schema_url_is_valid(tmp_path):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    settings = ClientSettings(
        remote_schema_url="http://testserver/graphq/", queries_path=queries_path
    )

    assert not settings.schema_path


def test_client_settings_without_schema_path_or_remote_schema_url_raises_exception(
    tmp_path,
):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    with pytest.raises(InvalidConfiguration):
        ClientSettings(queries_path=queries_path)


def test_client_settings_resolves_env_variable_for_remote_schema_header_with_prefix(
    tmp_path, mocker
):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    mocker.patch.dict(os.environ, {"TEST_VAR": "test_value"})

    settings = ClientSettings(
        queries_path=queries_path,
        remote_schema_url="https://test",
        remote_schema_headers={"Authorization": "$TEST_VAR"},
    )

    assert settings.remote_schema_headers["Authorization"] == "test_value"


def test_client_settings_doesnt_resolve_remote_schema_header_without_prefix(tmp_path):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    settings = ClientSettings(
        queries_path=queries_path,
        remote_schema_url="https://test",
        remote_schema_headers={"Authorization": "no_prefix"},
    )

    assert settings.remote_schema_headers["Authorization"] == "no_prefix"


def test_client_settings_raises_invalid_configuration_for_not_found_env_variable(
    tmp_path,
):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    with pytest.raises(InvalidConfiguration):
        ClientSettings(
            queries_path=queries_path,
            remote_schema_url="https://test",
            remote_schema_headers={"Authorization": "$TEST_VAR"},
        )


def test_client_settings_used_settings_message_returns_string_with_summary_of_data(
    tmp_path,
):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    base_client_file_content = """
    class BaseClient:
        pass
    """
    base_client_file_path = tmp_path / "base_client.py"
    base_client_file_path.write_text(dedent(base_client_file_content))
    settings = ClientSettings(
        schema_path=schema_path.as_posix(),
        queries_path=queries_path.as_posix(),
        base_client_name="BaseClient",
        base_client_file_path=base_client_file_path.as_posix(),
    )

    result = settings.used_settings_message

    assert settings.schema_path in result
    assert settings.queries_path in result
    assert settings.target_package_name in result
    assert settings.target_package_path in result
    assert settings.client_name in result
    assert settings.base_client_name in result
    assert settings.base_client_file_path in result
    assert settings.enums_module_name in result
    assert settings.input_types_module_name in result


def test_graphq_schema_settings_without_remote_schema_url_with_schema_path_is_valid(
    tmp_path,
):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()

    settings = GraphQLSchemaSettings(schema_path=schema_path.as_posix())

    assert not settings.remote_schema_url


def test_graphq_schema_settings_without_schema_path_with_remote_schema_url_is_valid():
    settings = GraphQLSchemaSettings(remote_schema_url="http://testserver/graphq/")

    assert not settings.schema_path


def test_graphql_schema_settings_with_target_file_path_with_py_extension_is_valid():
    settings = GraphQLSchemaSettings(
        remote_schema_url="http://testserver/graphq/",
        target_file_path="schema_file.py",
    )

    assert settings.target_file_path == "schema_file.py"
    assert settings.target_file_format == "py"


def test_graphql_schema_settings_with_target_file_with_graphql_extension_is_valid():
    settings = GraphQLSchemaSettings(
        remote_schema_url="http://testserver/graphq/",
        target_file_path="schema_file.graphql",
    )

    assert settings.target_file_path == "schema_file.graphql"
    assert settings.target_file_format == "graphql"


def test_graphql_schema_settings_with_target_file_path_with_gql_extension_is_valid():
    settings = GraphQLSchemaSettings(
        remote_schema_url="http://testserver/graphq/",
        target_file_path="schema_file.gql",
    )

    assert settings.target_file_path == "schema_file.gql"
    assert settings.target_file_format == "gql"


def test_graphql_schema_settings_target_file_format_is_lowercased():
    settings = GraphQLSchemaSettings(
        remote_schema_url="http://testserver/graphq/",
        target_file_path="schema_file.GQL",
    )

    assert settings.target_file_format == "gql"


def test_graphq_schema_settings_without_schema_path_or_remote_schema_url_is_not_valid():
    with pytest.raises(InvalidConfiguration):
        GraphQLSchemaSettings()


def test_graphql_schema_settings_raises_invalid_configuration_for_invalid_schema_path():
    with pytest.raises(InvalidConfiguration):
        GraphQLSchemaSettings(schema_path="not_exisitng.graphql")


def test_graphql_schema_settings_with_target_file_missing_extension_raises_exception():
    with pytest.raises(InvalidConfiguration):
        GraphQLSchemaSettings(
            remote_schema_url="http://testserver/graphq/",
            target_file_path="schema_file",
        )


def test_graphql_schema_settings_with_target_file_invalid_extension_raises_exception():
    with pytest.raises(InvalidConfiguration):
        GraphQLSchemaSettings(
            remote_schema_url="http://testserver/graphq/",
            target_file_path="schema_file.invalid",
        )


def test_graphql_schema_settings_with_invalid_schema_variable_name_raises_exception():
    with pytest.raises(InvalidConfiguration):
        GraphQLSchemaSettings(
            remote_schema_url="http://testserver/graphq/",
            schema_variable_name="!schema?",
        )


def test_graphql_schema_settings_with_invalid_type_map_variable_name_raises_exception():
    with pytest.raises(InvalidConfiguration):
        GraphQLSchemaSettings(
            remote_schema_url="http://testserver/graphq/",
            type_map_variable_name="1type_map",
        )
