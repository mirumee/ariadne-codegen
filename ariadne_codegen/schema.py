from pathlib import Path
from typing import Generator, Tuple

from graphql import (
    DefinitionNode,
    FragmentDefinitionNode,
    GraphQLSchema,
    GraphQLSyntaxError,
    OperationDefinitionNode,
    assert_valid_schema,
    build_ast_schema,
    parse,
)

from .exceptions import InvalidGraphqlSyntax


def filter_operations_definitions(
    definitions: Tuple[DefinitionNode, ...]
) -> list[OperationDefinitionNode]:
    """Return list including only operations definitions."""
    return [d for d in definitions if isinstance(d, OperationDefinitionNode)]


def filter_fragments_definitions(
    definitions: Tuple[DefinitionNode, ...]
) -> list[FragmentDefinitionNode]:
    """Return list including only fragments definitions."""
    return [d for d in definitions if isinstance(d, FragmentDefinitionNode)]


def get_graphql_queries(queries_path: str) -> Tuple[DefinitionNode, ...]:
    """Get graphql queries definitions build from provided path."""
    queries_str = load_graphql_files_from_path(Path(queries_path))
    queries_ast = parse(queries_str)
    return queries_ast.definitions


def get_graphql_schema(schema_path: str) -> GraphQLSchema:
    """Get graphql schema build from provided path."""
    schema_str = load_graphql_files_from_path(Path(schema_path))
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
