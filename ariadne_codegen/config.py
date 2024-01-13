from dataclasses import fields
from pathlib import Path
from typing import Dict, Optional
from warnings import simplefilter, warn

import toml

from .client_generators.scalars import ScalarData
from .exceptions import ConfigFileNotFound, MissingConfiguration
from .settings import ClientSettings, CommentsStrategy, GraphQLSchemaSettings

simplefilter("default", DeprecationWarning)


def get_config_file_path(file_name: str = "pyproject.toml") -> Path:
    """Get config file path. If not found raise exception."""
    directory = Path.cwd()
    while not directory.joinpath(file_name).exists():
        if directory == directory.parent:
            raise ConfigFileNotFound(f"Config file {file_name} not found.")
        directory = directory.parent
    return directory.joinpath(file_name).resolve()


def get_config_dict(config_file_name: Optional[str] = None) -> Dict:
    """Get config dict."""
    if config_file_name:
        config_file_path = get_config_file_path(config_file_name)
    else:
        config_file_path = get_config_file_path()

    return toml.load(config_file_path)


def get_client_settings(config_dict: Dict) -> ClientSettings:
    """Parse configuration dict and return ClientSettings instance."""
    section = get_section(config_dict).copy()
    settings_fields_names = {f.name for f in fields(ClientSettings)}
    try:
        section["scalars"] = {
            name: ScalarData(
                type_=data["type"],
                serialize=data.get("serialize"),
                parse=data.get("parse"),
                import_=data.get("import"),
            )
            for name, data in section.get("scalars", {}).items()
        }
    except KeyError as exc:
        raise MissingConfiguration(
            "Missing 'type' field for scalar definition"
        ) from exc

    try:
        if "include_comments" in section and isinstance(
            section["include_comments"], bool
        ):
            section["include_comments"] = (
                CommentsStrategy.TIMESTAMP.value
                if section["include_comments"]
                else CommentsStrategy.NONE.value
            )
            options = ", ".join(strategy.value for strategy in CommentsStrategy)
            warn(
                "Support for boolean 'include_comments' value has been deprecated "
                "and will be dropped in future release. "
                f"Instead use one of following options: {options}",
                DeprecationWarning,
                stacklevel=2,
            )

        return ClientSettings(
            **{
                key: value
                for key, value in section.items()
                if key in settings_fields_names
            }
        )
    except TypeError as exc:
        missing_fields = settings_fields_names.difference(section)
        raise MissingConfiguration(
            f"Missing configuration fields: {', '.join(missing_fields)}"
        ) from exc


def get_section(config_dict: Dict) -> Dict:
    """Get section from config dict."""
    tool_key = "tool"
    codegen_key = "ariadne-codegen"
    if tool_key in config_dict and codegen_key in config_dict.get(tool_key, {}):
        return config_dict[tool_key][codegen_key]

    if codegen_key in config_dict:
        warn(
            f"Support for [{codegen_key}] section has been deprecated "
            "and will be dropped in future release. "
            f"Instead use [{tool_key}.{codegen_key}].",
            DeprecationWarning,
            stacklevel=2,
        )
        return config_dict[codegen_key]

    raise MissingConfiguration(f"Config has no [{tool_key}.{codegen_key}] section.")


def get_graphql_schema_settings(config_dict: Dict) -> GraphQLSchemaSettings:
    """Parse configuration dict and return GraphQLSchemaSettings instance."""
    section = get_section(config_dict)
    settings_fields_names = {f.name for f in fields(GraphQLSchemaSettings)}
    try:
        return GraphQLSchemaSettings(
            **{
                key: value
                for key, value in section.items()
                if key in settings_fields_names
            }
        )
    except TypeError as exc:
        missing_fields = settings_fields_names.difference(section)
        raise MissingConfiguration(
            f"Missing configuration fields: {', '.join(missing_fields)}"
        ) from exc
