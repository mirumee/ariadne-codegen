import httpx
import pytest
from graphql import GraphQLSchema, OperationDefinitionNode, build_schema

from ariadne_codegen.exceptions import (
    IntrospectionError,
    InvalidGraphqlSyntax,
    InvalidOperationForSchema,
)
from ariadne_codegen.schema import (
    get_graphql_queries,
    get_graphql_schema_from_path,
    introspect_remote_schema,
    load_graphql_files_from_path,
    read_graphql_file,
    walk_graphql_files,
)


@pytest.fixture
def schema_str():
    return """
        type Query {
            test: Custom
        }

        type Custom {
            node: String
            default: String
        }
    """


@pytest.fixture
def extra_type_str():
    return """
        type User {
            name: String
        }
    """


@pytest.fixture
def test_query_str():
    return """
        query testQuery {
            test {
                node
                default
            }
        }
    """


@pytest.fixture
def test_query_2_str():
    return """
        query testQuery2 {
            test {
                node
                default
            }
        }
    """


@pytest.fixture
def single_file_schema(tmp_path_factory, schema_str):
    file_ = tmp_path_factory.mktemp("schema").joinpath("schema.graphql")
    file_.write_text(schema_str, encoding="utf-8")
    return file_


@pytest.fixture
def invalid_schema_file(tmp_path_factory):
    file_ = tmp_path_factory.mktemp("schema").joinpath("schema.graphql")
    schema_str = """
        type Query {
            test: String! @unknownDirective
        }
    """
    file_.write_text(schema_str, encoding="utf-8")
    return file_


@pytest.fixture
def invalid_syntax_schema_file(tmp_path_factory):
    file_ = tmp_path_factory.mktemp("schema").joinpath("schema.graphql")
    schema_str = """
        type Query {
            test: Custom

        type Custom {
            node: String
            default: String
        }
    """
    file_.write_text(schema_str, encoding="utf-8")
    return file_


@pytest.fixture
def schemas_directory(tmp_path_factory, schema_str, extra_type_str):
    schemas_dir = tmp_path_factory.mktemp("schemas")
    first_file = schemas_dir.joinpath("schema.graphql")
    first_file.write_text(schema_str, encoding="utf-8")
    second_file = schemas_dir.joinpath("user.graphql")
    second_file.write_text(extra_type_str, encoding="utf-8")
    return schemas_dir


@pytest.fixture
def schemas_nested_directories(tmp_path_factory, schema_str, extra_type_str):
    schemas_dir = tmp_path_factory.mktemp("schemas")
    nested_dir = schemas_dir.joinpath("nested")
    nested_dir.mkdir()
    first_file = schemas_dir.joinpath("schema.graphql")
    first_file.write_text(schema_str, encoding="utf-8")
    second_file = nested_dir.joinpath("user.graphql")
    second_file.write_text(extra_type_str, encoding="utf-8")
    return schemas_dir


@pytest.fixture
def path_fixture(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def single_file_query(tmp_path_factory, test_query_str):
    file_ = tmp_path_factory.mktemp("queries").joinpath("query1.graphql")
    file_.write_text(test_query_str, encoding="utf-8")
    return file_


@pytest.fixture
def invalid_syntax_query_file(tmp_path_factory):
    file_ = tmp_path_factory.mktemp("queries").joinpath("query.graphql")
    query_str = """
        query testQuery
            test {
                node
                default
            }
        }
    """
    file_.write_text(query_str, encoding="utf-8")
    return file_


@pytest.fixture
def invalid_query_for_schema_file(tmp_path_factory):
    file_ = tmp_path_factory.mktemp("queries").joinpath("query.graphql")
    query_str = """
        query testQuery {
            test {
                node
                default
            }
            anotherQuery
        }
    """
    file_.write_text(query_str, encoding="utf-8")
    return file_


@pytest.fixture
def queries_directory(tmp_path_factory, test_query_str, test_query_2_str):
    schemas_dir = tmp_path_factory.mktemp("queries")
    first_file = schemas_dir.joinpath("query1.graphql")
    first_file.write_text(test_query_str, encoding="utf-8")
    second_file = schemas_dir.joinpath("query2.graphql")
    second_file.write_text(test_query_2_str, encoding="utf-8")
    return schemas_dir


def test_read_graphql_file_returns_content_of_file(single_file_schema, schema_str):
    assert read_graphql_file(single_file_schema) == schema_str


def test_read_graphql_file_with_invalid_file_raises_invalid_graphql_syntax_exception(
    invalid_syntax_schema_file,
):
    with pytest.raises(InvalidGraphqlSyntax) as exc:
        read_graphql_file(invalid_syntax_schema_file)
    assert str(invalid_syntax_schema_file) in str(exc)


def test_walk_graphql_files_returns_graphql_files_from_directory(schemas_directory):
    assert sorted(f.name for f in walk_graphql_files(schemas_directory)) == sorted(
        ["schema.graphql", "user.graphql"]
    )


def test_walk_graphql_files_returns_graphql_files_from_nested_directory(
    schemas_nested_directories,
):
    assert sorted(
        f.name for f in walk_graphql_files(schemas_nested_directories)
    ) == sorted(["schema.graphql", "user.graphql"])


def test_load_graphql_files_from_path_returns_schema_from_single_file(
    single_file_schema, schema_str
):
    assert load_graphql_files_from_path(single_file_schema) == schema_str


def test_load_graphql_files_from_path_returns_schema_from_directory(
    schemas_directory, schema_str, extra_type_str
):
    content = load_graphql_files_from_path(schemas_directory)

    assert schema_str in content
    assert extra_type_str in content


def test_load_graphql_files_from_path_returns_schema_from_nested_directory(
    schemas_nested_directories, schema_str, extra_type_str
):
    content = load_graphql_files_from_path(schemas_nested_directories)

    assert schema_str in content
    assert extra_type_str in content


@pytest.mark.parametrize(
    "path_fixture",
    [
        "single_file_schema",
        "invalid_schema_file",
        "schemas_directory",
        "schemas_nested_directories",
    ],
    indirect=True,
)
def test_get_graphql_schema_from_path_returns_graphql_schema(path_fixture):
    assert isinstance(
        get_graphql_schema_from_path(path_fixture.as_posix()), GraphQLSchema
    )


def test_get_graphql_schema_from_path_with_invalid_syntax_raises_invalid_graphql_syntax(
    invalid_syntax_schema_file,
):
    with pytest.raises(InvalidGraphqlSyntax):
        get_graphql_schema_from_path(invalid_syntax_schema_file.as_posix())


def test_introspect_remote_schema_called_with_invalid_url_raises_introspection_error(
    mocker,
):
    mocker.patch(
        "ariadne_codegen.schema.httpx.post", side_effect=httpx.InvalidURL("msg")
    )

    with pytest.raises(IntrospectionError):
        introspect_remote_schema("invalid_url")


def test_introspect_remote_schema_raises_introspection_error_for_not_success_response(
    mocker,
):
    mocker.patch(
        "ariadne_codegen.schema.httpx.post",
        return_value=httpx.Response(status_code=400),
    )

    with pytest.raises(IntrospectionError) as exc:
        introspect_remote_schema("http://testserver/graphql/")

    assert "400" in exc.value.args[0]


def test_introspect_remote_schema_raises_introspection_error_for_not_json_response(
    mocker,
):
    mocker.patch(
        "ariadne_codegen.schema.httpx.post",
        return_value=httpx.Response(status_code=200, content="invalid_json"),
    )

    with pytest.raises(IntrospectionError):
        introspect_remote_schema("http://testserver/graphql/")


def test_introspect_remote_schema_raises_introspection_error_for_not_dict_response(
    mocker,
):
    mocker.patch(
        "ariadne_codegen.schema.httpx.post",
        return_value=httpx.Response(status_code=200, content="[]"),
    )

    with pytest.raises(IntrospectionError):
        introspect_remote_schema("http://testserver/graphql/")


def test_introspect_remote_schema_raises_introspection_error_for_json_without_data_key(
    mocker,
):
    mocker.patch(
        "ariadne_codegen.schema.httpx.post",
        return_value=httpx.Response(status_code=200, content='{"not_data": null}'),
    )

    with pytest.raises(IntrospectionError):
        introspect_remote_schema("http://testserver/graphql/")


def test_introspect_remote_schema_raises_introspection_error_for_graphql_errors(mocker):
    mocker.patch(
        "ariadne_codegen.schema.httpx.post",
        return_value=httpx.Response(
            status_code=200,
            content="""
            {
                "data": {},
                "errors": {
                    "message": "Error message",
                    "locations": [{"line": 6, "column": 7}],
                    "path": ["field1", "field2", 1, "id"]
                }
            }
            """,
        ),
    )

    with pytest.raises(IntrospectionError) as exc:
        introspect_remote_schema("http://testserver/graphql/")

    assert "Error message" in exc.value.args[0]


def test_introspect_remote_schema_raises_introspection_error_for_invalid_data_value(
    mocker,
):
    mocker.patch(
        "ariadne_codegen.schema.httpx.post",
        return_value=httpx.Response(
            status_code=200,
            content='{"data": []}',
        ),
    )

    with pytest.raises(IntrospectionError):
        introspect_remote_schema("http://testserver/graphql/")


def test_introspect_remote_schema_returns_introspection_result(mocker):
    mocker.patch(
        "ariadne_codegen.schema.httpx.post",
        return_value=httpx.Response(
            status_code=200,
            content='{"data": {"__schema": {}}}',
        ),
    )

    result = introspect_remote_schema("http://testserver/graphql/")

    assert result == {"__schema": {}}


def test_introspect_remote_schema_uses_provided_headers(mocker):
    mocked_post = mocker.patch(
        "ariadne_codegen.schema.httpx.post",
        return_value=httpx.Response(
            status_code=200,
            content='{"data": {"__schema": {}}}',
        ),
    )

    introspect_remote_schema("http://testserver/graphql/", headers={"test": "value"})

    assert mocked_post.called
    assert mocked_post.called_with(headers={"test": "value"})


@pytest.mark.parametrize("verify_ssl", [True, False])
def test_introspect_remote_schema_uses_provided_verify_ssl_flag(verify_ssl, mocker):
    mocked_post = mocker.patch(
        "ariadne_codegen.schema.httpx.post",
        return_value=httpx.Response(
            status_code=200, content='{"data": {"__schema": {}}}'
        ),
    )

    introspect_remote_schema("http://testserver/graphql/", verify_ssl=verify_ssl)

    assert mocked_post.called
    assert mocked_post.called_with(verify=verify_ssl)


def test_get_graphql_queries_returns_schema_definitions_from_single_file(
    single_file_query, schema_str
):
    queries = get_graphql_queries(
        single_file_query.as_posix(), build_schema(schema_str)
    )
    assert len(queries) == 1
    assert isinstance(queries[0], OperationDefinitionNode)
    assert queries[0].name
    assert queries[0].name.value == "testQuery"


def test_get_graphql_queries_returns_schema_definitions_from_directory(
    queries_directory, schema_str
):
    queries = get_graphql_queries(
        queries_directory.as_posix(), build_schema(schema_str)
    )
    assert len(queries) == 2
    assert isinstance(queries[0], OperationDefinitionNode)
    assert isinstance(queries[1], OperationDefinitionNode)
    assert queries[0].name
    assert queries[1].name
    assert queries[0].name.value == "testQuery"
    assert queries[1].name.value == "testQuery2"


def test_get_graphql_queries_with_invalid_file_raises_invalid_graphql_syntax_exception(
    invalid_syntax_query_file, schema_str
):
    with pytest.raises(InvalidGraphqlSyntax):
        get_graphql_queries(
            invalid_syntax_query_file.as_posix(), build_schema(schema_str)
        )


def test_get_graphql_queries_with_invalid_query_for_schema_raises_invalid_operation(
    invalid_query_for_schema_file, schema_str
):
    with pytest.raises(InvalidOperationForSchema):
        get_graphql_queries(
            invalid_query_for_schema_file.as_posix(), build_schema(schema_str)
        )
