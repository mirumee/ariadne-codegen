from pathlib import Path
from typing import Generator

from graphql import GraphQLSchema, assert_valid_schema, build_ast_schema, parse

from .config import settings


def get_graphql_schema() -> GraphQLSchema:
    """Get graphql schema build from path provided by settings."""
    schema_str = load_schema_from_path(Path(settings.schema_path))
    graphql_ast = parse(schema_str)
    schema: GraphQLSchema = build_ast_schema(graphql_ast)
    assert_valid_schema(schema)
    return schema


def load_schema_from_path(path: Path) -> str:
    """
    Get schema from given path.
    If path is a directory, collect schemas from multiple files.
    """
    if path.is_dir():
        schema_list = [read_graphql_file(f) for f in sorted(walk_graphql_files(path))]
        return "\n".join(schema_list)
    return read_graphql_file(path.resolve())


def walk_graphql_files(path: Path) -> Generator[Path, None, None]:
    """Find graphql files within given path."""
    extensions = (".graphql", ".graphqls", ".gql")
    for file_ in path.glob("**/*"):
        if file_.suffix in extensions:
            yield file_


def read_graphql_file(path: Path) -> str:
    """Return content of file."""
    with open(path, "r", encoding="utf-8") as graphql_file:
        return graphql_file.read()
