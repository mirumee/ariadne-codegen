import pytest

from graphql_sdk_gen.config import Settings, get_config_file_path, parse_config_file
from graphql_sdk_gen.exceptions import ConfigFileNotFound, MissingConfiguration

SCHEMA_FILENAME = "schema.graphql"
QUERIES_DIR = "queries"


@pytest.fixture(scope="session")
def config_file(tmp_path_factory):
    file_ = tmp_path_factory.mktemp("project").joinpath("pyproject.toml")
    schema_path = file_.parent.joinpath(SCHEMA_FILENAME)
    schema_path.touch()
    queries_path = file_.parent.joinpath(QUERIES_DIR)
    queries_path.mkdir()
    config = "\n".join(
        [
            "[graphql-sdk-gen]",
            f'schema_path = "{schema_path.as_posix()}"',
            f'queries_path = "{queries_path.as_posix()}"',
        ]
    )
    file_.write_text(config, encoding="utf-8")
    return file_


@pytest.fixture(scope="session")
def config_file_invalid_section(tmp_path_factory):
    file_ = tmp_path_factory.mktemp("project").joinpath("pyproject.toml")
    config = '[invalid-section]\nschema_path = "."'
    file_.write_text(config, encoding="utf-8")
    return file_


@pytest.fixture(scope="session")
def config_file_without_field(tmp_path_factory):
    file_ = tmp_path_factory.mktemp("project").joinpath("pyproject.toml")
    config = '[graphql-sdk-gen]\ninvalid_field = "."'
    file_.write_text(config, encoding="utf-8")
    return file_


def mock_cwd(mocker, path):
    mocker.patch("graphql_sdk_gen.config.Path.cwd", return_value=path)


def test__get_config_file_path__finds_file_in_cwd(config_file, mocker):
    mock_cwd(mocker, config_file.parent)
    assert get_config_file_path("pyproject.toml") == config_file


def test__get_config_file_path__finds_file_in_parent_directory(config_file, mocker):
    nested_dir = config_file.parent.joinpath("nested")
    mock_cwd(mocker, nested_dir)
    assert get_config_file_path("pyproject.toml") == config_file


def test__get_config_file_path__raises_exception_if_file_not_found(config_file, mocker):
    mock_cwd(mocker, config_file.parent)
    with pytest.raises(ConfigFileNotFound):
        get_config_file_path("invalid.toml")


def test__parse_config_file__returns_settings_object(config_file, mocker):
    mock_cwd(mocker, config_file.parent)
    settings = parse_config_file(config_file)
    assert isinstance(settings, Settings)
    assert settings.schema_path.endswith(SCHEMA_FILENAME)


def test__parse_config_file__without_section_raises_exception(
    config_file_invalid_section, mocker
):
    mock_cwd(mocker, config_file_invalid_section.parent)
    with pytest.raises(MissingConfiguration):
        parse_config_file(config_file_invalid_section)


def test__parse_config_file__without_required_field_raises_exception(
    config_file_without_field, mocker
):
    mock_cwd(mocker, config_file_without_field.parent)
    with pytest.raises(MissingConfiguration):
        parse_config_file(config_file_without_field)
