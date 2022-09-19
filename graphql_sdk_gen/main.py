import click

from graphql_sdk_gen.config import settings


@click.command()
@click.version_option()
def main():
    print(settings)
    print("hello world!")
