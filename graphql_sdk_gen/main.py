import sys

import click

from .config import settings
from .generators.package import PackageGenerator
from .schema import get_graphql_queries, get_graphql_schema


@click.command()
@click.version_option()
def main():
    schema = get_graphql_schema()
    queries = get_graphql_queries()
    sys.stdout.write(f"{settings}\n{schema}\n{queries}")

    package_generator = PackageGenerator(
        module_name=settings.target_package_name,
        target_path=settings.target_package_loc,
    )
    package_generator.generate()


if __name__ == "__main__":
    main()
