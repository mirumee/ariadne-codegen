import os
from pathlib import Path
from textwrap import dedent

import pytest

from ariadne_codegen.client_generators.dependencies import (
    async_base_client,
    async_base_client_no_upload,
    async_base_client_open_telemetry,
    async_base_client_open_telemetry_no_upload,
    base_client,
    base_client_no_upload,
    base_client_open_telemetry,
    base_client_open_telemetry_no_upload,
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
    "async_client, opentelemetry_client, multipart_uploads,"
    " expected_name, expected_path, expected_module_name",
    [
        (
            True,
            True,
            True,
            "AsyncBaseClientOpenTelemetry",
            async_base_client_open_telemetry.__file__,
            "async_base_client_open_telemetry",
        ),
        (
            True,
            True,
            False,
            "AsyncBaseClientOpenTelemetry",
            async_base_client_open_telemetry_no_upload.__file__,
            "async_base_client_open_telemetry",
        ),
        (
            True,
            False,
            True,
            "AsyncBaseClient",
            async_base_client.__file__,
            "async_base_client",
        ),
        (
            True,
            False,
            False,
            "AsyncBaseClient",
            async_base_client_no_upload.__file__,
            "async_base_client",
        ),
        (
            False,
            True,
            True,
            "BaseClientOpenTelemetry",
            base_client_open_telemetry.__file__,
            "base_client_open_telemetry",
        ),
        (
            False,
            True,
            False,
            "BaseClientOpenTelemetry",
            base_client_open_telemetry_no_upload.__file__,
            "base_client_open_telemetry",
        ),
        (False, False, True, "BaseClient", base_client.__file__, "base_client"),
        (
            False,
            False,
            False,
            "BaseClient",
            base_client_no_upload.__file__,
            "base_client",
        ),
    ],
)
def test_client_settings_sets_correct_default_values_for_base_client_name_and_path(
    tmp_path,
    async_client,
    opentelemetry_client,
    multipart_uploads,
    expected_name,
    expected_path,
    expected_module_name,
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
        multipart_uploads=multipart_uploads,
    )

    assert settings.base_client_name == expected_name
    assert settings.base_client_file_path == Path(expected_path).as_posix()
    assert settings.base_client_module_name == expected_module_name


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


@pytest.mark.parametrize(
    "configured_header, expected_header",
    [
        ("$TEST_VAR", "test_value"),
        ("Bearer $TEST_VAR", "Bearer test_value"),
        ("Bearer: $TEST_VAR", "Bearer: test_value"),
        ("Bearer: ${TEST_VAR}", "Bearer: test_value"),
        pytest.param(
            "$NOT_SET_VAR",
            "",
            marks=pytest.mark.xfail(raises=InvalidConfiguration),
        ),
    ],
)
def test_client_settings_resolves_env_variable_for_remote_schema_header_with_prefix(
    tmp_path,
    mocker,
    configured_header,
    expected_header,
):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    mocker.patch.dict(os.environ, {"TEST_VAR": "test_value"})

    settings = ClientSettings(
        queries_path=queries_path,
        remote_schema_url="https://test",
        remote_schema_headers={"Authorization": configured_header},
    )

    assert settings.remote_schema_headers["Authorization"] == expected_header


def test_client_settings_resolves_multiple_embedded_env_vars_in_remote_schema_header(
    tmp_path, mocker
):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    mocker.patch.dict(os.environ, {"TEST_FOO": "foo_val", "TEST_BAR": "bar_val"})

    settings = ClientSettings(
        queries_path=queries_path,
        remote_schema_url="https://test",
        remote_schema_headers={"Authorization": "Bearer $TEST_FOO $TEST_BAR"},
    )

    assert settings.remote_schema_headers["Authorization"] == "Bearer foo_val bar_val"


@pytest.mark.parametrize(
    "configured_url, expected_url",
    [
        ("$TEST_VAR", "test_value"),
        ("https://${TEST_VAR}/graphql", "https://test_value/graphql"),
        ("https://$TEST_VAR/graphql", "https://test_value/graphql"),
        ("https://TEST_VAR/graphql", "https://TEST_VAR/graphql"),
        pytest.param(
            "https://${NOT_SET_VAR}/graphql",
            "",
            marks=pytest.mark.xfail(raises=InvalidConfiguration),
        ),
    ],
)
def test_client_settings_resolves_env_variable_for_remote_schema_url(
    tmp_path,
    mocker,
    configured_url,
    expected_url,
):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    mocker.patch.dict(os.environ, {"TEST_VAR": "test_value"})

    settings = ClientSettings(
        queries_path=queries_path,
        remote_schema_url=configured_url,
    )

    assert settings.remote_schema_url == expected_url


@pytest.mark.parametrize(
    "configured_header, expected_header",
    [
        # Malformed: only $VAR is replaced, trailing } stays literal
        ("Bearer $TEST_VAR}", "Bearer test_value}"),
        # Malformed: no closing brace, so no match - left unchanged
        ("${TEST_VAR", "${TEST_VAR"),
        # Variable name must start with letter/underscore: $1WOOT not matched
        ("$1WOOT", "$1WOOT"),
        # Leading underscore is allowed
        ("$_TEST_VAR", "underscore_value"),
        # Braced form with suffix (shell-like ${VAR}suffix)
        ("${TEST_VAR}suffix", "test_valuesuffix"),
    ],
)
def test_client_settings_env_var_resolution_edge_cases_in_headers(
    tmp_path,
    mocker,
    configured_header,
    expected_header,
):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    mocker.patch.dict(
        os.environ,
        {"TEST_VAR": "test_value", "_TEST_VAR": "underscore_value"},
    )

    settings = ClientSettings(
        queries_path=queries_path,
        remote_schema_url="https://test",
        remote_schema_headers={"Authorization": configured_header},
    )

    assert settings.remote_schema_headers["Authorization"] == expected_header


@pytest.mark.parametrize(
    "configured_url, expected_url",
    [
        ("https://${TEST_VAR", "https://${TEST_VAR"),
        ("$TEST_VAR}/path", "test_value}/path"),
    ],
)
def test_client_settings_env_var_resolution_edge_cases_in_url(
    tmp_path,
    mocker,
    configured_url,
    expected_url,
):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    mocker.patch.dict(os.environ, {"TEST_VAR": "test_value"})

    settings = ClientSettings(
        queries_path=queries_path,
        remote_schema_url=configured_url,
    )

    assert settings.remote_schema_url == expected_url


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


def test_client_settings_include_typename_default_value(tmp_path):
    """Test that include_typename defaults to True."""
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    settings = ClientSettings(
        schema_path=schema_path.as_posix(),
        queries_path=queries_path.as_posix(),
    )

    assert settings.include_typename is True


def test_client_settings_include_typename_can_be_set_to_false(tmp_path):
    """Test that include_typename can be set to False."""
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    settings = ClientSettings(
        schema_path=schema_path.as_posix(),
        queries_path=queries_path.as_posix(),
        include_typename=False,
    )

    assert settings.include_typename is False


def test_client_settings_include_typename_can_be_set_to_true(tmp_path):
    """Test that include_typename can be explicitly set to True."""
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    settings = ClientSettings(
        schema_path=schema_path.as_posix(),
        queries_path=queries_path.as_posix(),
        include_typename=True,
    )

    assert settings.include_typename is True


def test_using_remote_schema_true_when_only_remote_schema_url_is_provided(tmp_path):
    """
    Test that using_remote_schema is True when only remote_schema_url is provided.
    """
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    settings = ClientSettings(
        remote_schema_url="http://testserver/graphql/",
        queries_path=queries_path.as_posix(),
    )

    assert settings.using_remote_schema is True


def test_using_remote_schema_false_when_only_schema_path_is_provided(tmp_path):
    """
    Test that using_remote_schema is False when only schema_path is provided.
    """
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

    assert settings.using_remote_schema is False


def test_client_settings_with_schema_path_and_remote_schema_url_raises_invalid_configuration(
    tmp_path,
):
    """
    Test that providing both schema_path and remote_schema_url is rejected:
    only one schema source may be selected at a time.
    """
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    with pytest.raises(InvalidConfiguration):
        ClientSettings(
            schema_path=schema_path.as_posix(),
            remote_schema_url="http://testserver/graphql/",
            queries_path=queries_path.as_posix(),
        )


def test_introspection_settings_defaults(tmp_path):
    """
    Test that introspection settings have the correct default values.
    """
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    settings = ClientSettings(
        remote_schema_url="http://testserver/graphql/",
        queries_path=queries_path.as_posix(),
    )

    opts = settings.introspection_settings
    assert opts.descriptions is False
    assert opts.input_value_deprecation is False
    assert opts.specified_by_url is False
    assert opts.schema_description is False
    assert opts.directive_is_repeatable is False
    assert opts.input_object_one_of is False


def test_introspection_settings_overrides_are_mapped(tmp_path):
    """
    Test that introspection settings overrides are correctly mapped.
    """
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    settings = ClientSettings(
        remote_schema_url="http://testserver/graphql/",
        queries_path=queries_path.as_posix(),
        introspection_descriptions=True,
        introspection_input_value_deprecation=True,
        introspection_specified_by_url=True,
        introspection_schema_description=True,
        introspection_directive_is_repeatable=True,
        introspection_input_object_one_of=True,
    )

    opts = settings.introspection_settings
    assert opts.descriptions is True
    assert opts.input_value_deprecation is True
    assert opts.specified_by_url is True
    assert opts.schema_description is True
    assert opts.directive_is_repeatable is True
    assert opts.input_object_one_of is True


def test_client_settings_used_settings_message_includes_introspection(
    tmp_path,
):
    """
    Test that used_settings_message includes introspection settings when remote schema
    is used.
    """
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    remote_settings = ClientSettings(
        remote_schema_url="http://testserver/graphql/",
        queries_path=queries_path.as_posix(),
        introspection_schema_description=True,
    )
    assert "Introspection settings:" in remote_settings.used_settings_message
    assert "schema_description=true" in remote_settings.used_settings_message

    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()

    base_client_file_content = """
    class BaseClient:
        pass
    """
    base_client_file_path = tmp_path / "base_client.py"
    base_client_file_path.write_text(dedent(base_client_file_content))

    local_settings = ClientSettings(
        schema_path=schema_path.as_posix(),
        queries_path=queries_path.as_posix(),
        base_client_name="BaseClient",
        base_client_file_path=base_client_file_path.as_posix(),
        introspection_schema_description=True,
    )
    assert "Introspection settings:" not in local_settings.used_settings_message


def test_graphql_schema_settings_used_settings_message_includes_introspection(
    tmp_path,
):
    """
    Test that used_settings_message includes introspection settings when remote schema
    is used.
    """
    remote_settings = GraphQLSchemaSettings(
        remote_schema_url="http://testserver/graphql/",
        introspection_specified_by_url=True,
    )
    assert "Introspection settings:" in remote_settings.used_settings_message
    assert "specified_by_url=true" in remote_settings.used_settings_message
    assert "descriptions=false" in remote_settings.used_settings_message

    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()

    local_settings = GraphQLSchemaSettings(
        schema_path=schema_path.as_posix(),
        introspection_specified_by_url=True,
    )
    assert "Introspection settings:" not in local_settings.used_settings_message


def test_client_settings_with_schema_paths_is_valid(tmp_path):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    settings = ClientSettings(
        schema_paths=["pkg.get_files", "./schemas/"],
        queries_path=queries_path.as_posix(),
    )

    assert settings.schema_paths == ["pkg.get_files", "./schemas/"]


def test_graphql_schema_settings_with_schema_paths_is_valid():
    settings = GraphQLSchemaSettings(schema_paths=["pkg.SCHEMA_DIR"])

    assert settings.schema_paths == ["pkg.SCHEMA_DIR"]


def test_client_settings_with_schema_path_and_schema_paths_raises_invalid_configuration(
    tmp_path,
):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    with pytest.raises(InvalidConfiguration):
        ClientSettings(
            schema_path=schema_path.as_posix(),
            schema_paths=["pkg.get_files"],
            queries_path=queries_path.as_posix(),
        )


def test_graphql_schema_settings_with_schema_path_and_schema_paths_raises_invalid_configuration(
    tmp_path,
):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()

    with pytest.raises(InvalidConfiguration):
        GraphQLSchemaSettings(
            schema_path=schema_path.as_posix(),
            schema_paths=["pkg.get_files"],
        )


def test_client_settings_with_schema_paths_and_remote_schema_url_raises_invalid_configuration(
    tmp_path,
):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    with pytest.raises(InvalidConfiguration):
        ClientSettings(
            schema_paths=["pkg.get_files"],
            remote_schema_url="http://testserver/graphql/",
            queries_path=queries_path.as_posix(),
        )


def test_client_settings_without_any_schema_source_raises_invalid_configuration(
    tmp_path,
):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    with pytest.raises(InvalidConfiguration):
        ClientSettings(queries_path=queries_path.as_posix())


def test_graphql_schema_settings_without_any_schema_source_raises_invalid_configuration():
    with pytest.raises(InvalidConfiguration):
        GraphQLSchemaSettings()


def test_using_remote_schema_false_when_schema_paths_provided(tmp_path):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    settings = ClientSettings(
        schema_paths=["pkg.get_files"],
        queries_path=queries_path.as_posix(),
    )

    assert settings.using_remote_schema is False


def test_client_settings_schema_source_returns_schema_paths_joined(tmp_path):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    settings = ClientSettings(
        schema_paths=["pkg.get_files", "./extra/"],
        queries_path=queries_path.as_posix(),
    )

    assert settings.schema_source == "pkg.get_files, ./extra/"


def test_client_settings_used_settings_message_includes_schema_paths(tmp_path):
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    settings = ClientSettings(
        schema_paths=["pkg.get_files", "./schemas/"],
        queries_path=queries_path.as_posix(),
    )

    result = settings.used_settings_message
    assert "pkg.get_files" in result
    assert "./schemas/" in result


def test_graphql_schema_settings_used_settings_message_includes_schema_paths():
    settings = GraphQLSchemaSettings(schema_paths=["pkg.SCHEMA_DIR"])

    result = settings.used_settings_message
    assert "pkg.SCHEMA_DIR" in result
