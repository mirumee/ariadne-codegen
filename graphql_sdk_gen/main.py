import click

from .config import settings
from .schema import get_graphql_queries, get_graphql_schema


@click.command()
@click.version_option()
def main():
    print(settings)
    schema = get_graphql_schema()
    queries = get_graphql_queries()
    print(schema)
    print(queries)


if __name__ == "__main__":
    main()
