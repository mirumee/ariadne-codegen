import pytest

from ariadne_codegen.config import Settings, get_config_file_path, parse_config_file
from ariadne_codegen.exceptions import ConfigFileNotFound, MissingConfiguration

SCHEMA_FILENAME = "schema.graphql"
QUERIES_DIR = "queries"


@pytest.fixture
def config_file(tmp_path_factory):
    file_ = tmp_path_factory.mktemp("project").joinpath("pyproject.toml")
    schema_path = file_.parent.joinpath(SCHEMA_FILENAME)
    schema_path.touch()
    queries_path = file_.parent.joinpath(QUERIES_DIR)
    queries_path.mkdir()
    config = "\n".join(
        [
            "[ariadne-codegen]",
            f'schema_path = "{schema_path.as_posix()}"',
            f'queries_path = "{queries_path.as_posix()}"',
            "[ariadne-codegen.scalars.ID]",
            'type = "str"',
            'parse = "parse_id"',
            'serialize = "serialize_id"',
            'import = ".custom_scalars"',
        ]
    )
    file_.write_text(config, encoding="utf-8")
    return file_


@pytest.fixture
def config_file_invalid_section(tmp_path_factory):
    file_ = tmp_path_factory.mktemp("project").joinpath("pyproject.toml")
    config = '[invalid-section]\nschema_path = "."'
    file_.write_text(config, encoding="utf-8")
    return file_


@pytest.fixture
def config_file_without_field(tmp_path_factory):
    file_ = tmp_path_factory.mktemp("project").joinpath("pyproject.toml")
    config = '[ariadne-codegen]\ninvalid_field = "."'
    file_.write_text(config, encoding="utf-8")
    return file_


@pytest.fixture
def config_file_invalid_scalar(tmp_path_factory):
    file_ = tmp_path_factory.mktemp("project").joinpath("pyproject.toml")
    schema_path = file_.parent.joinpath(SCHEMA_FILENAME)
    schema_path.touch()
    queries_path = file_.parent.joinpath(QUERIES_DIR)
    queries_path.mkdir()
    config = "\n".join(
        [
            "[ariadne-codegen]",
            f'schema_path = "{schema_path.as_posix()}"',
            f'queries_path = "{queries_path.as_posix()}"',
            "[ariadne-codegen.scalars.ID]",
            'invalid_key = "str"',
        ]
    )
    file_.write_text(config, encoding="utf-8")
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


def test_parse_config_file_returns_settings_object(config_file, mocker):
    mock_cwd(mocker, config_file.parent)
    settings = parse_config_file(config_file)
    assert isinstance(settings, Settings)
    assert settings.schema_path.endswith(SCHEMA_FILENAME)


def test_parse_config_file_without_section_raises_missing_configuration_exception(
    config_file_invalid_section, mocker
):
    mock_cwd(mocker, config_file_invalid_section.parent)
    with pytest.raises(MissingConfiguration):
        parse_config_file(config_file_invalid_section)


def test_parse_config_file_without_needed_field_raises_missing_configuration_exception(
    config_file_without_field, mocker
):
    mock_cwd(mocker, config_file_without_field.parent)
    with pytest.raises(MissingConfiguration):
        parse_config_file(config_file_without_field)


def test_parse_config_file_with_invalid_scalar_section_raises_missing_configuration(
    config_file_invalid_scalar, mocker
):
    mock_cwd(mocker, config_file_invalid_scalar.parent)
    with pytest.raises(MissingConfiguration):
        parse_config_file(config_file_invalid_scalar)
