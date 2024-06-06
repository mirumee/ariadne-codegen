import enum
import os
from dataclasses import dataclass, field
from keyword import iskeyword
from pathlib import Path
from textwrap import dedent
from typing import Dict, List

from .client_generators.constants import (
    DEFAULT_ASYNC_BASE_CLIENT_NAME,
    DEFAULT_ASYNC_BASE_CLIENT_OPEN_TELEMETRY_NAME,
    DEFAULT_ASYNC_BASE_CLIENT_OPEN_TELEMETRY_PATH,
    DEFAULT_ASYNC_BASE_CLIENT_PATH,
    DEFAULT_BASE_CLIENT_NAME,
    DEFAULT_BASE_CLIENT_OPEN_TELEMETRY_NAME,
    DEFAULT_BASE_CLIENT_OPEN_TELEMETRY_PATH,
    DEFAULT_BASE_CLIENT_PATH,
)
from .client_generators.scalars import ScalarData
from .exceptions import InvalidConfiguration


class CommentsStrategy(str, enum.Enum):
    NONE = "none"
    STABLE = "stable"
    TIMESTAMP = "timestamp"


class Strategy(str, enum.Enum):
    CLIENT = "client"
    GRAPHQL_SCHEMA = "graphqlschema"


@dataclass
class BaseSettings:
    schema_path: str = ""
    remote_schema_url: str = ""
    remote_schema_headers: dict = field(default_factory=dict)
    remote_schema_verify_ssl: bool = True
    enable_custom_operations: bool = False
    plugins: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.schema_path and not self.remote_schema_url:
            raise InvalidConfiguration(
                "Schema source not provided. Use schema_path or remote_schema_url"
            )

        if self.schema_path:
            assert_path_exists(self.schema_path)

        self.remote_schema_headers = resolve_headers(self.remote_schema_headers)


@dataclass
class ClientSettings(BaseSettings):
    queries_path: str = ""
    target_package_name: str = "graphql_client"
    target_package_path: str = field(default_factory=lambda: Path.cwd().as_posix())
    client_name: str = "Client"
    client_file_name: str = "client"
    base_client_name: str = ""
    base_client_file_path: str = ""
    enums_module_name: str = "enums"
    input_types_module_name: str = "input_types"
    fragments_module_name: str = "fragments"
    include_comments: CommentsStrategy = field(default=CommentsStrategy.STABLE)
    convert_to_snake_case: bool = True
    include_all_inputs: bool = True
    include_all_enums: bool = True
    async_client: bool = True
    opentelemetry_client: bool = False
    files_to_include: List[str] = field(default_factory=list)
    scalars: Dict[str, ScalarData] = field(default_factory=dict)

    def __post_init__(self):
        if not self.queries_path and not self.enable_custom_operations:
            raise TypeError("__init__ missing 1 required argument: 'queries_path'")
        super().__post_init__()

        try:
            self.include_comments = CommentsStrategy(self.include_comments)
        except ValueError as exc:
            valid_options = ", ".join(strategy.value for strategy in CommentsStrategy)
            raise InvalidConfiguration(
                f"'{self.include_comments}' is not a valid choice. "
                f"Valid options are: {valid_options}"
            ) from exc

        self._set_default_base_client_data()

        for name, data in self.scalars.items():
            data.graphql_name = name

        assert_path_exists(self.queries_path)

        assert_string_is_valid_python_identifier(self.target_package_name)
        assert_path_is_valid_directory(self.target_package_path)

        assert_string_is_valid_python_identifier(self.client_name)
        assert_string_is_valid_python_identifier(self.client_file_name)
        assert_string_is_valid_python_identifier(self.base_client_name)
        assert_path_exists(self.base_client_file_path)
        assert_path_is_valid_file(self.base_client_file_path)
        assert_class_is_defined_in_file(
            Path(self.base_client_file_path), self.base_client_name
        )

        assert_string_is_valid_python_identifier(self.enums_module_name)
        assert_string_is_valid_python_identifier(self.input_types_module_name)

        for file_path in self.files_to_include:
            assert_path_is_valid_file(file_path)

    def _set_default_base_client_data(self):
        default_clients_map = {
            (True, True): (
                DEFAULT_ASYNC_BASE_CLIENT_OPEN_TELEMETRY_PATH,
                DEFAULT_ASYNC_BASE_CLIENT_OPEN_TELEMETRY_NAME,
            ),
            (True, False): (
                DEFAULT_ASYNC_BASE_CLIENT_PATH,
                DEFAULT_ASYNC_BASE_CLIENT_NAME,
            ),
            (False, True): (
                DEFAULT_BASE_CLIENT_OPEN_TELEMETRY_PATH,
                DEFAULT_BASE_CLIENT_OPEN_TELEMETRY_NAME,
            ),
            (False, False): (
                DEFAULT_BASE_CLIENT_PATH,
                DEFAULT_BASE_CLIENT_NAME,
            ),
        }
        if not self.base_client_name and not self.base_client_file_path:
            path, name = default_clients_map[
                (self.async_client, self.opentelemetry_client)
            ]
            self.base_client_name = name
            self.base_client_file_path = path.as_posix()

    @property
    def schema_source(self) -> str:
        return self.schema_path if self.schema_path else self.remote_schema_url

    @property
    def used_settings_message(self) -> str:
        snake_case_msg = (
            "Converting fields and arguments name to snake case."
            if self.convert_to_snake_case
            else "Not converting fields and arguments name to snake case."
        )
        async_client_msg = (
            "Generating async client."
            if self.async_client
            else "Generating not async client."
        )
        files_to_include_list = ",".join(self.files_to_include)
        files_to_include_msg = (
            f"Coping following files into package: {files_to_include_list}"
            if self.files_to_include
            else "No files to copy."
        )
        plugins_list = ",".join(self.plugins)
        plugins_msg = (
            f"Plugins to use: {plugins_list}"
            if self.plugins
            else "No plugin is being used."
        )
        return dedent(
            f"""\
            Selected strategy: {Strategy.CLIENT}
            Using schema from '{self.schema_path or self.remote_schema_url}'.
            Reading queries from '{self.queries_path}'.
            Using '{self.target_package_name}' as package name.
            Generating package into '{self.target_package_path}'.
            Using '{self.client_name}' as client name.
            Using '{self.base_client_name}' as base client class.
            Coping base client class from '{self.base_client_file_path}'.
            Generating enums into '{self.enums_module_name}.py'.
            Generating inputs into '{self.input_types_module_name}.py'.
            Generating fragments into '{self.fragments_module_name}.py'.
            Comments type: {self.include_comments.value}
            {snake_case_msg}
            {async_client_msg}
            {files_to_include_msg}
            {plugins_msg}
            """
        )


@dataclass
class GraphQLSchemaSettings(BaseSettings):
    target_file_path: str = "schema.py"
    schema_variable_name: str = "schema"
    type_map_variable_name: str = "type_map"

    def __post_init__(self):
        super().__post_init__()

        assert_string_is_valid_schema_target_filename(self.target_file_path)
        assert_string_is_valid_python_identifier(self.schema_variable_name)
        assert_string_is_valid_python_identifier(self.type_map_variable_name)

    @property
    def used_settings_message(self):
        plugins_list = ",".join(self.plugins)
        plugins_msg = (
            f"Plugins to use: {plugins_list}"
            if self.plugins
            else "No plugin is being used."
        )

        if self.target_file_format == "py":
            return dedent(
                f"""\
                Selected strategy: {Strategy.GRAPHQL_SCHEMA}
                Using schema from {self.schema_path or self.remote_schema_url}
                Saving graphql schema to: {self.target_file_path}
                Using {self.schema_variable_name} as variable name for schema.
                Using {self.type_map_variable_name} as variable name for type map.
                {plugins_msg}
                """
            )

        return dedent(
            f"""\
            Selected strategy: {Strategy.GRAPHQL_SCHEMA}
            Using schema from {self.schema_path or self.remote_schema_url}
            Saving graphql schema to: {self.target_file_path}
            {plugins_msg}
            """
        )

    @property
    def target_file_format(self):
        return Path(self.target_file_path).suffix[1:].lower()


def assert_path_exists(path: str):
    if not Path(path).exists():
        raise InvalidConfiguration(f"Provided path {path} doesn't exist.")


def assert_path_is_valid_directory(path: str):
    if not Path(path).is_dir():
        raise InvalidConfiguration(f"Provided path {path} isn't a directory.")


def assert_path_is_valid_file(path: str):
    if not Path(path).is_file():
        raise InvalidConfiguration(f"Provided path {path} isn't a file.")


def assert_string_is_valid_schema_target_filename(filename: str):
    file_type = Path(filename).suffix
    if not file_type:
        raise InvalidConfiguration(
            f"Provided file name {filename} is missing a file type."
        )

    file_type = file_type[1:].lower()
    if file_type not in ("py", "graphql", "gql"):
        raise InvalidConfiguration(
            f"Provided file name {filename} has an invalid type {file_type}."
            " Valid types are py, graphql and gql."
        )


def assert_string_is_valid_python_identifier(name: str):
    if not name.isidentifier() and not iskeyword(name):
        raise InvalidConfiguration(
            f"Provided name {name} cannot be used as python identifier."
        )


def resolve_headers(headers: Dict) -> Dict:
    return {key: get_header_value(value) for key, value in headers.items()}


def get_header_value(value: str) -> str:
    env_var_prefix = "$"
    if value.startswith(env_var_prefix):
        env_var_name = value.lstrip(env_var_prefix)
        var_value = os.environ.get(env_var_name)
        if not var_value:
            raise InvalidConfiguration(
                f"Environment variable {env_var_name} not found."
            )
        return var_value

    return value


def assert_class_is_defined_in_file(file_path: Path, class_name: str):
    file_content = file_path.read_text()
    if f"class {class_name}" not in file_content:
        raise InvalidConfiguration(f"Cannot import {class_name} from {file_path}")
