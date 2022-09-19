from pathlib import Path

import toml

from graphql_sdk_gen.exceptions import ConfigFileNotFound, MissingConfiguration


def get_config_file_path(file_name: str = "pyproject.toml") -> Path:
    """Get config file path. If not found raise exception."""
    directory = Path.cwd()
    while not (file_path := directory.joinpath(file_name)).exists():
        if directory == directory.parent:
            raise ConfigFileNotFound(f"Config file {file_name} not found.")
        else:
            directory = directory.parent
    return file_path


def parse_config_file(file_path: Path, key: str = "graphql-sdk-gen") -> dict:
    """Parse configuration from toml file. Raise exception if section was not found."""
    config = toml.load(file_path)
    try:
        return config[key]
    except KeyError as exc:
        raise MissingConfiguration(f"File {file_path} has no [{key}] section.") from exc


settings = parse_config_file(get_config_file_path())
