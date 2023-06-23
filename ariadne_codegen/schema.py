from pathlib import Path
from typing import Dict, Generator, List, Optional, Tuple, cast

import httpx
from graphql import (
    DefinitionNode,
    DirectiveLocation,
    FragmentDefinitionNode,
    GraphQLArgument,
    GraphQLDirective,
    GraphQLSchema,
    GraphQLString,
    GraphQLSyntaxError,
    IntrospectionQuery,
    NoUnusedFragmentsRule,
    OperationDefinitionNode,
    build_ast_schema,
    build_client_schema,
    get_introspection_query,
    parse,
    specified_rules,
    validate,
)

from .client_generators.constants import MIXIN_FROM_NAME, MIXIN_IMPORT_NAME, MIXIN_NAME
from .exceptions import (
    IntrospectionError,
    InvalidGraphqlSyntax,
    InvalidOperationForSchema,
)


def filter_operations_definitions(
    definitions: Tuple[DefinitionNode, ...]
) -> List[OperationDefinitionNode]:
    """Return list including only operations definitions."""
    return [d for d in definitions if isinstance(d, OperationDefinitionNode)]


def filter_fragments_definitions(
    definitions: Tuple[DefinitionNode, ...]
) -> List[FragmentDefinitionNode]:
    """Return list including only fragments definitions."""
    return [d for d in definitions if isinstance(d, FragmentDefinitionNode)]


def get_graphql_queries(
    queries_path: str, schema: GraphQLSchema
) -> Tuple[DefinitionNode, ...]:
    """Get graphql queries definitions build from provided path."""
    queries_str = load_graphql_files_from_path(Path(queries_path))
    queries_ast = parse(queries_str)
    validation_errors = validate(
        schema=schema,
        document_ast=queries_ast,
        rules=[r for r in specified_rules if r is not NoUnusedFragmentsRule],
    )
    if validation_errors:
        raise InvalidOperationForSchema(
            "\n\n".join(error.message for error in validation_errors)
        )
    return queries_ast.definitions


def get_graphql_schema_from_url(
    url: str, headers: Optional[Dict[str, str]] = None, verify_ssl: bool = True
) -> GraphQLSchema:
    return build_client_schema(
        introspect_remote_schema(url=url, headers=headers, verify_ssl=verify_ssl),
        assume_valid=True,
    )


def introspect_remote_schema(
    url: str, headers: Optional[Dict[str, str]] = None, verify_ssl: bool = True
) -> IntrospectionQuery:
    try:
        response = httpx.post(
            url,
            json={"query": get_introspection_query(descriptions=False)},
            headers=headers,
            verify=verify_ssl,
        )
    except httpx.InvalidURL as exc:
        raise IntrospectionError(f"Invalid remote schema url: {url}") from exc

    if not response.is_success:
        raise IntrospectionError(
            "Failure of remote schema introspection. "
            f"HTTP status code: {response.status_code}"
        )

    try:
        response_json = response.json()
    except ValueError as exc:
        raise IntrospectionError("Introspection result is not a valid json.") from exc

    if (not isinstance(response_json, dict)) or ("data" not in response_json):
        raise IntrospectionError("Invalid introspection result format.")

    errors = response_json.get("errors")
    if errors:
        raise IntrospectionError(f"Introspection errors: {errors}")

    data = response_json["data"]
    if not isinstance(data, dict):
        raise IntrospectionError("Invalid data key in introspection result.")

    return cast(IntrospectionQuery, data)


def get_graphql_schema_from_path(schema_path: str) -> GraphQLSchema:
    """Get graphql schema build from provided path."""
    schema_str = load_graphql_files_from_path(Path(schema_path))
    graphql_ast = parse(schema_str)
    schema: GraphQLSchema = build_ast_schema(graphql_ast, assume_valid=True)
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


def add_mixin_directive_to_schema(schema: GraphQLSchema) -> GraphQLSchema:
    if MIXIN_NAME in {d.name for d in schema.directives}:
        return schema

    schema.directives += (
        GraphQLDirective(
            name=MIXIN_NAME,
            locations=[DirectiveLocation.FIELD, DirectiveLocation.FRAGMENT_DEFINITION],
            args={
                MIXIN_IMPORT_NAME: GraphQLArgument(type_=GraphQLString),
                MIXIN_FROM_NAME: GraphQLArgument(type_=GraphQLString),
            },
            is_repeatable=True,
        ),
    )
    return schema
