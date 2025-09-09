from textwrap import dedent

import pytest

from ariadne_codegen.client_generators.scalars import ScalarData
from ariadne_codegen.config import (
    get_client_settings,
    get_config_dict,
    get_config_file_path,
    get_graphql_schema_settings,
    get_section,
)
from ariadne_codegen.exceptions import ConfigFileNotFound, MissingConfiguration
from ariadne_codegen.settings import (
    ClientSettings,
    CommentsStrategy,
    GraphQLSchemaSettings,
)


@pytest.fixture
def client_config_file(tmp_path_factory):
    file_ = tmp_path_factory.mktemp("project").joinpath("pyproject.toml")
    schema_path = file_.parent.joinpath("schema.graphql")
    schema_path.touch()
    queries_path = file_.parent.joinpath("queries")
    queries_path.mkdir()
    config = """
        [tool.ariadne-codegen]
        schema_path = "schema.graphql"
        queries_path = "queries"
    """
    file_.write_text(dedent(config), encoding="utf-8")
    return file_


def mock_cwd(mocker, path):
    mocker.patch("ariadne_codegen.config.Path.cwd", return_value=path)


def test_get_config_file_path_finds_file_in_cwd(client_config_file, mocker):
    mock_cwd(mocker, client_config_file.parent)
    assert get_config_file_path("pyproject.toml") == client_config_file


def test_get_config_file_path_finds_file_in_parent_directory(
    client_config_file, mocker
):
    nested_dir = client_config_file.parent.joinpath("nested")
    mock_cwd(mocker, nested_dir)
    assert get_config_file_path("pyproject.toml") == client_config_file


def test_get_config_file_path_raises_config_file_not_found_exception_if_file_not_found(
    client_config_file, mocker
):
    mock_cwd(mocker, client_config_file.parent)
    with pytest.raises(ConfigFileNotFound):
        get_config_file_path("invalid.toml")


def test_get_config_dict_returns_file_content_as_dict(client_config_file, mocker):
    mock_cwd(mocker, client_config_file.parent)

    config_dict = get_config_dict()

    assert isinstance(config_dict, dict)


def test_get_config_dict_reads_file_with_provided_name(client_config_file, mocker):
    mock_cwd(mocker, client_config_file.parent)
    client_config_file.rename(client_config_file.parent / "test.toml")

    config_dict = get_config_dict("test.toml")

    assert isinstance(config_dict, dict)


def test_get_client_settings_returns_client_settings_object(tmp_path):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    config_dict = {
        "tool": {
            "ariadne-codegen": {
                "schema_path": schema_path.as_posix(),
                "queries_path": queries_path.as_posix(),
                "scalars": {
                    "ID": {
                        "type": "str",
                        "parse": "parse_id",
                        "serialize": "serialize_id",
                        "import": ".custom_scalars",
                    }
                },
            }
        }
    }
    settings = get_client_settings(config_dict)

    assert isinstance(settings, ClientSettings)
    assert settings.schema_path == schema_path.as_posix()
    assert settings.queries_path == queries_path.as_posix()
    assert settings.scalars == {
        "ID": ScalarData(
            type_="str",
            serialize="serialize_id",
            parse="parse_id",
            import_=".custom_scalars",
            graphql_name="ID",
        )
    }

    # Regression test for #256: don't mutate config_dict's scalars
    assert config_dict["tool"]["ariadne-codegen"]["scalars"] == {
        "ID": {
            "type": "str",
            "parse": "parse_id",
            "serialize": "serialize_id",
            "import": ".custom_scalars",
        },
    }


def test_get_client_settings_without_section_raises_missing_configuration_exception():
    config_dict = {"invalid-section": {"schema_path": "."}}

    with pytest.raises(MissingConfiguration):
        get_client_settings(config_dict)


def testget_client_settings_without_field_raises_missing_configuration_exception():
    config_dict = {"tool": {"ariadne-codegen": {"invalid_field": "."}}}

    with pytest.raises(MissingConfiguration):
        get_client_settings(config_dict)


def test_get_client_settings_with_invalid_scalar_section_raises_missing_configuration(
    tmp_path,
):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    config_dict = {
        "tool": {
            "ariadne-codegen": {
                "schema_path": schema_path.as_posix(),
                "queries_path": queries_path.as_posix(),
                "scalars": {"ID": {"invalid_key": "str"}},
            }
        }
    }

    with pytest.raises(MissingConfiguration):
        get_client_settings(config_dict)


def test_get_client_settings_returns_client_settings_object_ignoring_extra_fields(
    tmp_path,
):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    config_dict = {
        "tool": {
            "ariadne-codegen": {
                "schema_path": schema_path.as_posix(),
                "queries_path": queries_path.as_posix(),
                "extra_key": "extra",
            }
        }
    }
    settings = get_client_settings(config_dict)

    assert isinstance(settings, ClientSettings)
    assert settings.schema_path == schema_path.as_posix()
    assert settings.queries_path == queries_path.as_posix()


@pytest.mark.parametrize(
    "include_comments, expected_result",
    [(True, CommentsStrategy.TIMESTAMP), (False, CommentsStrategy.NONE)],
)
def test_get_client_settings_raises_deprecation_warning_for_boolean_include_comments(
    tmp_path, include_comments, expected_result
):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    config_dict = {
        "tool": {
            "ariadne-codegen": {
                "schema_path": schema_path.as_posix(),
                "queries_path": queries_path.as_posix(),
                "include_comments": include_comments,
            }
        }
    }

    with pytest.deprecated_call():
        settings = get_client_settings(config_dict)

    assert settings.include_comments == expected_result


def test_get_section_returns_correct_dictionary_from_tool_key():
    section_dict = {"schema_path": ".", "queries_path": "."}
    config_dict = {"tool": {"ariadne-codegen": section_dict}}

    assert get_section(config_dict) == section_dict


def test_get_section_returns_dict_from_codegen_key_and_raises_deprecation_warning():
    section_dict = {"schema_path": ".", "queries_path": "."}
    config_dict = {"ariadne-codegen": section_dict}

    with pytest.deprecated_call():
        result = get_section(config_dict)

    assert result == section_dict


def test_get_graphql_schema_settings_returns_graphql_schema_settings_object(tmp_path):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    config_dict = {"tool": {"ariadne-codegen": {"schema_path": schema_path.as_posix()}}}
    settings = get_graphql_schema_settings(config_dict)

    assert isinstance(settings, GraphQLSchemaSettings)
    assert settings.schema_path == schema_path.as_posix()


def test_get_graphql_schema_settings_returns_settings_object_ignoring_extra_fields(
    tmp_path,
):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    config_dict = {
        "tool": {
            "ariadne-codegen": {
                "schema_path": schema_path.as_posix(),
                "extra_field": "extra",
            }
        }
    }
    settings = get_graphql_schema_settings(config_dict)

    assert isinstance(settings, GraphQLSchemaSettings)
    assert settings.schema_path == schema_path.as_posix()



def test_get_client_settings_with_include_typename_false(tmp_path):
    """Test that include_typename=False is properly parsed from config."""
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    config_dict = {
        "tool": {
            "ariadne-codegen": {
                "schema_path": schema_path.as_posix(),
                "queries_path": queries_path.as_posix(),
                "include_typename": False,
            }
        }
    }
    settings = get_client_settings(config_dict)

    assert isinstance(settings, ClientSettings)
    assert settings.include_typename is False


def test_get_client_settings_with_include_typename_true(tmp_path):
    """Test that include_typename=True is properly parsed from config."""
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    config_dict = {
        "tool": {
            "ariadne-codegen": {
                "schema_path": schema_path.as_posix(),
                "queries_path": queries_path.as_posix(),
                "include_typename": True,
            }
        }
    }
    settings = get_client_settings(config_dict)

    assert isinstance(settings, ClientSettings)
    assert settings.include_typename is True


def test_get_client_settings_without_include_typename_defaults_to_true(tmp_path):
    """Test that include_typename defaults to True when not specified in config."""
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    config_dict = {
        "tool": {
            "ariadne-codegen": {
                "schema_path": schema_path.as_posix(),
                "queries_path": queries_path.as_posix(),
            }
        }
    }
    settings = get_client_settings(config_dict)

    assert isinstance(settings, ClientSettings)
    assert settings.include_typename is True

