import click

from .config import settings
from .schema import get_graphql_schema


@click.command()
@click.version_option()
def main():
    print(settings)
    schema = get_graphql_schema()
