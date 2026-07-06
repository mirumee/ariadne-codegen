import importlib
from collections.abc import Generator, Sequence
from dataclasses import asdict
from pathlib import Path
from typing import Optional, cast

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
from typing_extensions import Any

from .client_generators.constants import MIXIN_FROM_NAME, MIXIN_IMPORT_NAME, MIXIN_NAME
from .exceptions import (
    IntrospectionError,
    InvalidConfiguration,
    InvalidGraphqlSyntax,
    InvalidOperationForSchema,
)
from .settings import IntrospectionSettings, assert_path_exists


def filter_operations_definitions(
    definitions: tuple[DefinitionNode, ...],
) -> list[OperationDefinitionNode]:
    """Return list including only operations definitions."""
    return [d for d in definitions if isinstance(d, OperationDefinitionNode)]


def filter_fragments_definitions(
    definitions: tuple[DefinitionNode, ...],
) -> list[FragmentDefinitionNode]:
    """Return list including only fragments definitions."""
    return [d for d in definitions if isinstance(d, FragmentDefinitionNode)]


def get_graphql_queries(
    queries_path: str,
    schema: GraphQLSchema,
    skip_rules: Sequence[Any] = (NoUnusedFragmentsRule,),
) -> tuple[DefinitionNode, ...]:
    """Get graphql queries definitions build from provided path."""
    queries_str = load_graphql_files_from_path(Path(queries_path))
    queries_ast = parse(queries_str)
    validation_errors = validate(
        schema=schema,
        document_ast=queries_ast,
        rules=[r for r in specified_rules if r not in skip_rules],
    )
    if validation_errors:
        raise InvalidOperationForSchema(
            "\n\n".join(error.message for error in validation_errors)
        )
    return queries_ast.definitions


def get_graphql_schema_from_url(
    url: str,
    headers: Optional[dict[str, str]] = None,
    verify_ssl: bool = True,
    timeout: float = 5,
    introspection_settings: Optional[IntrospectionSettings] = None,
) -> GraphQLSchema:
    return build_client_schema(
        introspect_remote_schema(
            url=url,
            headers=headers,
            verify_ssl=verify_ssl,
            timeout=timeout,
            introspection_settings=introspection_settings,
        ),
        assume_valid=True,
    )


def introspect_remote_schema(
    url: str,
    headers: Optional[dict[str, str]] = None,
    verify_ssl: bool = True,
    timeout: float = 5,
    introspection_settings: Optional[IntrospectionSettings] = None,
) -> IntrospectionQuery:
    # If introspection settings are not provided, use default values.
    settings = introspection_settings or IntrospectionSettings()
    query = get_introspection_query(**asdict(settings))
    try:
        response = httpx.post(
            url,
            json={"query": query},
            headers=headers,
            verify=verify_ssl,
            timeout=timeout,
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

    if not isinstance(response_json, dict):
        raise IntrospectionError("Invalid introspection result format.")

    errors = response_json.get("errors")
    if errors:
        raise IntrospectionError(f"Introspection errors: {errors}")

    data = response_json.get("data")
    if not isinstance(data, dict):
        raise IntrospectionError("Invalid data key in introspection result.")

    return cast(IntrospectionQuery, data)


def _read_graphql_files(paths: list[Path]) -> str:
    """Read and concatenate the contents of the given graphql files."""
    return "\n".join(read_graphql_file(path) for path in paths)


def _build_schema_from_str(schema_str: str) -> GraphQLSchema:
    """Build a GraphQLSchema from concatenated schema source."""
    graphql_ast = parse(schema_str)
    schema: GraphQLSchema = build_ast_schema(graphql_ast, assume_valid=True)
    return schema


def get_graphql_schema_from_path(schema_path: str) -> GraphQLSchema:
    """Get graphql schema built from a single file or directory path."""
    return get_graphql_schema_from_paths([schema_path])


def resolve_schema_paths(sources: list[str]) -> list[Path]:
    """Resolve a list of schema sources to concrete file paths.

    Each entry is first tried as a local filesystem path - a directory (searched
    recursively for graphql files) or a file. If it points to neither, it is
    treated as a dotted Python import path (e.g. ``pkg.SCHEMA_DIR`` or
    ``pkg.get_schema_files``); an import path that cannot be resolved raises
    ``InvalidConfiguration``.
    """
    result: list[Path] = []
    for source in sources:
        path = Path(source)
        if path.is_dir():
            result.extend(sorted(walk_graphql_files(path)))
        elif path.is_file():
            result.append(path)
        else:
            resolved = _resolve_import_source(source)
            for resolved_path in resolved:
                assert_path_exists(resolved_path.as_posix())
            result.extend(resolved)
    return result


def _resolve_import_source(source: str) -> list[Path]:
    """Resolve a dotted Python import path to schema file paths.

    The imported object may be a callable returning a list of paths, or a string
    / ``Path`` pointing to a file or a directory.
    """
    try:
        module_path, attr = source.rsplit(".", 1)
        module = importlib.import_module(module_path)
        obj = getattr(module, attr)
    except (ImportError, AttributeError, ValueError) as exc:
        raise InvalidConfiguration(
            f"Could not resolve schema source '{source}'. It is neither an "
            f"existing file/directory nor an importable attribute: {exc}."
        ) from exc

    if callable(obj):
        return [Path(f) for f in obj()]
    if isinstance(obj, (str, Path)):
        obj_path = Path(obj)
        if obj_path.is_dir():
            return sorted(walk_graphql_files(obj_path))
        return [obj_path]
    raise InvalidConfiguration(
        f"Schema source '{source}' resolved to {type(obj).__name__}; expected a "
        "path string, a Path, or a callable returning a list of paths."
    )


def get_graphql_schema_from_paths(schema_paths: list[str]) -> GraphQLSchema:
    """Get graphql schema built from multiple sources (paths or import paths)."""
    resolved = resolve_schema_paths(schema_paths)
    return _build_schema_from_str(_read_graphql_files(resolved))


def load_graphql_files_from_path(path: Path) -> str:
    """
    Get schema from given path.
    If path is a directory, collect schemas from multiple files.
    """
    if path.is_dir():
        return _read_graphql_files(sorted(walk_graphql_files(path)))
    return read_graphql_file(path.resolve())


def walk_graphql_files(path: Path) -> Generator[Path, None, None]:
    """Find graphql files within given path."""
    extensions = (".graphql", ".graphqls", ".gql")
    for file_ in path.glob("**/*"):
        if file_.suffix in extensions:
            yield file_


def read_graphql_file(path: Path) -> str:
    """Return content of file."""
    with open(path, encoding="utf-8") as graphql_file:
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
                MIXIN_IMPORT_NAME: GraphQLArgument(
                    type_=GraphQLString,  # ty: ignore[invalid-argument-type]
                ),
                MIXIN_FROM_NAME: GraphQLArgument(
                    type_=GraphQLString,  # ty: ignore[invalid-argument-type]
                ),
            },
            is_repeatable=True,
        ),
    )
    return schema
