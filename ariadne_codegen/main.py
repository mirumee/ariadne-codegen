import sys

import click
from graphql import assert_valid_schema

from .client_generators.package import get_package_generator
from .config import get_client_settings, get_config_dict, get_graphql_schema_settings
from .graphql_schema_generators.schema import (
    generate_graphql_schema_graphql_file,
    generate_graphql_schema_python_file,
)
from .plugins.explorer import get_plugins_types
from .plugins.manager import PluginManager
from .schema import (
    add_mixin_directive_to_schema,
    filter_fragments_definitions,
    filter_operations_definitions,
    get_graphql_queries,
    get_graphql_schema_from_path,
    get_graphql_schema_from_url,
)
from .settings import Strategy


@click.command()  # type: ignore
@click.version_option()
@click.option("--config", default=None, help="Path to custom configuration file.")
@click.argument(
    "strategy",
    default=Strategy.CLIENT,
    type=click.Choice([e.value for e in Strategy]),
    required=False,
)
def main(strategy=Strategy.CLIENT, config=None):
    config_dict = get_config_dict(config)
    if strategy == Strategy.CLIENT:
        client(config_dict)

    if strategy == Strategy.GRAPHQL_SCHEMA:
        graphql_schema(config_dict)


def client(config_dict):
    settings = get_client_settings(config_dict)

    if settings.schema_path:
        schema = get_graphql_schema_from_path(settings.schema_path)
    else:
        schema = get_graphql_schema_from_url(
            url=settings.remote_schema_url,
            headers=settings.remote_schema_headers,
            verify_ssl=settings.remote_schema_verify_ssl,
        )

    plugin_manager = PluginManager(
        schema=schema,
        config_dict=config_dict,
        plugins_types=get_plugins_types(settings.plugins),
    )
    schema = add_mixin_directive_to_schema(schema)
    schema = plugin_manager.process_schema(schema)
    assert_valid_schema(schema)

    fragments = []
    queries = []
    if settings.queries_path:
        definitions = get_graphql_queries(settings.queries_path, schema)
        queries = filter_operations_definitions(definitions)
        fragments = filter_fragments_definitions(definitions)

    sys.stdout.write(settings.used_settings_message)

    package_generator = get_package_generator(
        schema=schema,
        fragments=fragments,
        settings=settings,
        plugin_manager=plugin_manager,
    )
    for query in queries:
        package_generator.add_operation(query)
    generated_files = package_generator.generate()

    sys.stdout.write("\nGenerated files:\n  " + "\n  ".join(generated_files) + "\n")


def graphql_schema(config_dict):
    settings = get_graphql_schema_settings(config_dict)

    schema = (
        get_graphql_schema_from_path(settings.schema_path)
        if settings.schema_path
        else get_graphql_schema_from_url(
            url=settings.remote_schema_url,
            headers=settings.remote_schema_headers,
            verify_ssl=settings.remote_schema_verify_ssl,
        )
    )
    plugin_manager = PluginManager(
        schema=schema,
        config_dict=config_dict,
        plugins_types=get_plugins_types(settings.plugins),
    )
    schema = plugin_manager.process_schema(schema)
    assert_valid_schema(schema)

    sys.stdout.write(settings.used_settings_message)

    if settings.target_file_format == "py":
        generate_graphql_schema_python_file(
            schema=schema,
            target_file_path=settings.target_file_path,
            type_map_name=settings.type_map_variable_name,
            schema_variable_name=settings.schema_variable_name,
        )
    else:
        generate_graphql_schema_graphql_file(
            schema=schema,
            target_file_path=settings.target_file_path,
        )
