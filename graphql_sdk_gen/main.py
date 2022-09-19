import click

from graphql_sdk_gen.config import settings
from graphql_sdk_gen.schema import get_graphql_schema


@click.command()
@click.version_option()
def main():
    print(settings)
    schema = get_graphql_schema()
