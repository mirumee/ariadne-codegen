from pathlib import Path
from textwrap import dedent

import pytest

import ariadne_codegen.generators.dependencies.async_base_client
import ariadne_codegen.generators.dependencies.base_client
from ariadne_codegen.config import Settings, get_used_settings_message
from ariadne_codegen.exceptions import InvalidConfiguration


def test_settings_with_base_client_defined_in_file_creates_object(tmp_path):
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

    Settings(
        schema_path=schema_path.as_posix(),
        queries_path=queries_path.as_posix(),
        base_client_name="BaseClient",
        base_client_file_path=base_client_file_path.as_posix(),
    )


def test_settings_with_not_importable_base_client_file_raises_invalid_configuration(
    tmp_path,
):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    base_client_file_path = tmp_path / "invalid_file.txt"
    base_client_file_path.write_text("invalid content")

    with pytest.raises(InvalidConfiguration):
        Settings(
            schema_path=schema_path.as_posix(),
            queries_path=queries_path.as_posix(),
            base_client_file_path=base_client_file_path.as_posix(),
            base_client_name="BaseClient",
        )


def test_settings_with_base_client_not_defined_in_file_raises_configuration_exception(
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
        Settings(
            schema_path=schema_path.as_posix(),
            queries_path=queries_path.as_posix(),
            base_client_name="OtherClient",
            base_client_file_path=base_client_file_path.as_posix(),
        )


@pytest.mark.parametrize(
    "async_client,expected_name,expected_path",
    [
        (
            True,
            "AsyncBaseClient",
            Path(ariadne_codegen.generators.dependencies.async_base_client.__file__),
        ),
        (
            False,
            "BaseClient",
            Path(ariadne_codegen.generators.dependencies.base_client.__file__),
        ),
    ],
)
def test_settings_sets_correct_default_values_for_base_client_name_and_path(
    tmp_path, async_client, expected_name, expected_path
):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()

    settings = Settings(
        schema_path=schema_path, queries_path=queries_path, async_client=async_client
    )

    assert settings.base_client_name == expected_name
    assert settings.base_client_file_path == expected_path.as_posix()


def test_get_used_settings_message_returns_string_with_data_from_given_settings(
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
    settings = Settings(
        schema_path=schema_path.as_posix(),
        queries_path=queries_path.as_posix(),
        base_client_name="BaseClient",
        base_client_file_path=base_client_file_path.as_posix(),
    )

    result = get_used_settings_message(settings)

    assert settings.schema_path in result
    assert settings.queries_path in result
    assert settings.target_package_name in result
    assert settings.target_package_path in result
    assert settings.client_name in result
    assert settings.base_client_name in result
    assert settings.base_client_file_path in result
    assert settings.enums_module_name in result
    assert settings.input_types_module_name in result
