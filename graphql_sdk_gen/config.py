import importlib.util
from dataclasses import dataclass, field, fields
from keyword import iskeyword
from pathlib import Path

import toml

from .exceptions import ConfigFileNotFound, InvalidConfiguration, MissingConfiguration


@dataclass(frozen=True)
class Settings:
    schema_path: str
    queries_path: str
    target_package_name: str = "graphql_client"
    target_package_path: str = field(default_factory=lambda: Path.cwd().as_posix())
    client_name: str = "Client"
    client_file_name: str = "client"
    base_client_name: str = "BaseClient"
    base_client_file_path: str = field(
        default_factory=lambda: Path(__file__)
        .parent.joinpath("generators", "base_client.py")
        .as_posix()
    )
    schema_types_module_name: str = "schema_types"
    enums_module_name: str = "enums"
    input_types_module_name: str = "input_types"

    def __post_init__(self):
        self._assert_path_exists(self.schema_path)
        self._assert_path_exists(self.queries_path)

        self._assert_string_is_valid_python_identifier(self.target_package_name)
        self._assert_path_is_valid_directory(self.target_package_path)

        self._assert_string_is_valid_python_identifier(self.client_name)
        self._assert_string_is_valid_python_identifier(self.client_file_name)
        self._assert_string_is_valid_python_identifier(self.base_client_name)
        self._assert_path_exists(self.base_client_file_path)
        self._assert_path_is_valid_file(self.base_client_file_path)
        self._assert_class_is_defined_in_file(
            Path(self.base_client_file_path), self.base_client_name
        )

        self._assert_string_is_valid_python_identifier(self.schema_types_module_name)
        self._assert_string_is_valid_python_identifier(self.enums_module_name)
        self._assert_string_is_valid_python_identifier(self.input_types_module_name)

    def _assert_path_exists(self, path: str):
        if not Path(path).exists():
            raise InvalidConfiguration(f"Provided path {path} doesn't exist.")

    def _assert_path_is_valid_directory(self, path: str):
        if not Path(path).is_dir():
            raise InvalidConfiguration(f"Provided path {path} isn't a directory.")

    def _assert_path_is_valid_file(self, path: str):
        if not Path(path).is_file():
            raise InvalidConfiguration(f"Provided path {path} isn't a file.")

    def _assert_string_is_valid_python_identifier(self, name: str):
        if not name.isidentifier() and not iskeyword(name):
            raise InvalidConfiguration(
                f"Provided name {name} cannot be used as python indetifier"
            )

    def _assert_class_is_defined_in_file(self, file_path: Path, class_name: str):
        spec = importlib.util.spec_from_file_location(
            file_path.stem, file_path.as_posix()
        )
        if not spec or not spec.loader:
            raise InvalidConfiguration(f"Cannot import from {file_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        class_ = getattr(module, class_name, None)
        if not class_:
            raise InvalidConfiguration(f"Cannot import {class_name} from {file_path}")


def get_config_file_path(file_name: str = "pyproject.toml") -> Path:
    """Get config file path. If not found raise exception."""
    directory = Path.cwd()
    while not (file_path := directory.joinpath(file_name)).exists():
        if directory == directory.parent:
            raise ConfigFileNotFound(f"Config file {file_name} not found.")
        directory = directory.parent
    return file_path.resolve()


def parse_config_file(
    file_path: Path, section_key: str = "graphql-sdk-gen"
) -> Settings:
    """
    Parse configuration from toml file. Raise exception if section or key was not found.
    """
    config = toml.load(file_path)
    if section_key not in config:
        raise MissingConfiguration(f"File {file_path} has no [{section_key}] section.")

    try:
        return Settings(**config[section_key])
    except TypeError as exc:
        expected_fields = {f.name for f in fields(Settings)}
        missing_fields = expected_fields.difference(config[section_key])
        raise MissingConfiguration(
            f"Missing configuration fields: {', '.join(missing_fields)}"
        ) from exc


settings = parse_config_file(get_config_file_path())
