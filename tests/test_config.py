from textwrap import dedent

import pytest

from ariadne_codegen.client_generators.scalars import ScalarData
from ariadne_codegen.config import (
    Settings,
    get_config_dict,
    get_config_file_path,
    get_section,
    parse_config_dict,
)
from ariadne_codegen.exceptions import ConfigFileNotFound, MissingConfiguration


@pytest.fixture
def config_file(tmp_path_factory):
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


def test_get_config_file_path_finds_file_in_cwd(config_file, mocker):
    mock_cwd(mocker, config_file.parent)
    assert get_config_file_path("pyproject.toml") == config_file


def test_get_config_file_path_finds_file_in_parent_directory(config_file, mocker):
    nested_dir = config_file.parent.joinpath("nested")
    mock_cwd(mocker, nested_dir)
    assert get_config_file_path("pyproject.toml") == config_file


def test_get_config_file_path_raises_config_file_not_found_exception_if_file_not_found(
    config_file, mocker
):
    mock_cwd(mocker, config_file.parent)
    with pytest.raises(ConfigFileNotFound):
        get_config_file_path("invalid.toml")


def test_get_config_dict_returns_file_content_as_dict(config_file, mocker):
    mock_cwd(mocker, config_file.parent)

    config_dict = get_config_dict()

    assert isinstance(config_dict, dict)


def test_get_config_dict_reads_file_with_provided_name(config_file, mocker):
    mock_cwd(mocker, config_file.parent)
    config_file.rename(config_file.parent / "test.toml")

    config_dict = get_config_dict("test.toml")

    assert isinstance(config_dict, dict)


def test_parse_config_dict_returns_settings_object(tmp_path):
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
    settings = parse_config_dict(config_dict)

    assert isinstance(settings, Settings)
    assert settings.schema_path == schema_path.as_posix()
    assert settings.queries_path == queries_path.as_posix()
    assert settings.scalars == {
        "ID": ScalarData(
            type_="str",
            serialize="serialize_id",
            parse="parse_id",
            import_=".custom_scalars",
        )
    }


def test_parse_config_dict_without_section_raises_missing_configuration_exception():
    config_dict = {"invalid-section": {"schema_path": "."}}

    with pytest.raises(MissingConfiguration):
        parse_config_dict(config_dict)


def test_parse_config_dict_without_field_raises_missing_configuration_exception():
    config_dict = {"tool": {"ariadne-codegen": {"invalid_field": "."}}}

    with pytest.raises(MissingConfiguration):
        parse_config_dict(config_dict)


def test_parse_config_dict_with_invalid_scalar_section_raises_missing_configuration(
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
        parse_config_dict(config_dict)


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
