from pathlib import Path
from typing import Generator, Tuple

from graphql import (
    DefinitionNode,
    GraphQLSchema,
    GraphQLSyntaxError,
    assert_valid_schema,
    build_ast_schema,
    parse,
)

from .config import settings
from .exceptions import InvalidGraphqlSyntax


def get_graphql_queries() -> Tuple[DefinitionNode, ...]:
    """Get graphql queries definitions build from path provided by settings."""
    queries_str = load_graphql_files_from_path(Path(settings.queries_path))
    queries_ast = parse(queries_str)
    return queries_ast.definitions


def get_graphql_schema() -> GraphQLSchema:
    """Get graphql schema build from path provided by settings."""
    schema_str = load_graphql_files_from_path(Path(settings.schema_path))
    graphql_ast = parse(schema_str)
    schema: GraphQLSchema = build_ast_schema(graphql_ast)
    assert_valid_schema(schema)
    return schema


def load_graphql_files_from_path(path: Path) -> str:
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
        schema = graphql_file.read()
    try:
        parse(schema)
    except GraphQLSyntaxError as exc:
        raise InvalidGraphqlSyntax(f"Invalid graphql syntax in file {path}") from exc
    return schema
