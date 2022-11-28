import sys

import click

from .config import get_used_settings_message, settings
from .generators.package import PackageGenerator
from .schema import (
    filter_fragments_definitions,
    filter_operations_definitions,
    get_graphql_queries,
    get_graphql_schema,
)


@click.command()
@click.version_option()
def main():
    schema = get_graphql_schema()
    definitions = get_graphql_queries()
    queries = filter_operations_definitions(definitions)
    fragments = filter_fragments_definitions(definitions)

    sys.stdout.write(get_used_settings_message(settings))

    package_generator = PackageGenerator(
        package_name=settings.target_package_name,
        target_path=settings.target_package_path,
        schema=schema,
        client_name=settings.client_name,
        client_file_name=settings.client_file_name,
        base_client_name=settings.base_client_name,
        base_client_file_path=settings.base_client_file_path,
        schema_types_module_name=settings.schema_types_module_name,
        input_types_module_name=settings.input_types_module_name,
        queries_source=settings.queries_path,
        schema_source=settings.schema_path,
        include_comments=settings.include_comments,
        fragments=fragments,
    )
    for query in queries:
        package_generator.add_query(query)
    generated_files = package_generator.generate()

    sys.stdout.write("\nGenerated files:\n  " + "\n  ".join(generated_files) + "\n")


if __name__ == "__main__":
    main()
