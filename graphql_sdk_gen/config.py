from dataclasses import dataclass, fields
from pathlib import Path

import toml

from graphql_sdk_gen.exceptions import ConfigFileNotFound, MissingConfiguration


@dataclass
class Settings:
    schema_path: str


def get_config_file_path(file_name: str = "pyproject.toml") -> Path:
    """Get config file path. If not found raise exception."""
    directory = Path.cwd()
    while not (file_path := directory.joinpath(file_name)).exists():
        if directory == directory.parent:
            raise ConfigFileNotFound(f"Config file {file_name} not found.")
        else:
            directory = directory.parent
    return file_path


def parse_config_file(
    file_path: Path, section_key: str = "graphql-sdk-gen"
) -> Settings:
    """Parse configuration from toml file. Raise exception if section or key was not found."""
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
