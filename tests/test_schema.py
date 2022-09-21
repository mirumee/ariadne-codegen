import pytest
from graphql import GraphQLSchema, GraphQLSyntaxError
from graphql_sdk_gen.config import Settings
from graphql_sdk_gen.schema import (
    get_graphql_schema,
    load_schema_from_path,
    read_graphql_file,
    walk_graphql_files,
)

FIRST_SCHEMA = """
    type Query {
        test: Custom
    }

    type Custom {
        node: String
        default: String
    }
"""

SECOND_SCHEMA = """
    type User {
        name: String
    }
"""

INCORRECT_SCHEMA = """
    type Query {
        test: Custom

    type Custom {
        node: String
        default: String
    }
"""

FIRST_FILENAME = "base.graphql"
SECOND_FILENAME = "user.graphql"


@pytest.fixture(scope="session")
def single_file_schema(tmp_path_factory):
    file_ = tmp_path_factory.mktemp("schema").joinpath("schema.graphql")
    file_.write_text(FIRST_SCHEMA, encoding="utf-8")
    return file_


@pytest.fixture(scope="session")
def incorrect_schema_file(tmp_path_factory):
    file_ = tmp_path_factory.mktemp("schema").joinpath("schema.graphql")
    file_.write_text(INCORRECT_SCHEMA, encoding="utf-8")
    return file_


@pytest.fixture(scope="session")
def schemas_directory(tmp_path_factory):
    schemas_dir = tmp_path_factory.mktemp("schemas")
    first_file = schemas_dir.joinpath(FIRST_FILENAME)
    first_file.write_text(FIRST_SCHEMA, encoding="utf-8")
    second_file = schemas_dir.joinpath(SECOND_FILENAME)
    second_file.write_text(SECOND_SCHEMA, encoding="utf-8")
    return schemas_dir


@pytest.fixture(scope="session")
def schemas_nested_directories(tmp_path_factory):
    schemas_dir = tmp_path_factory.mktemp("schemas")
    nested_dir = schemas_dir.joinpath("nested")
    nested_dir.mkdir()
    first_file = schemas_dir.joinpath(FIRST_FILENAME)
    first_file.write_text(FIRST_SCHEMA, encoding="utf-8")
    second_file = nested_dir.joinpath(SECOND_FILENAME)
    second_file.write_text(SECOND_SCHEMA, encoding="utf-8")
    return schemas_dir


@pytest.fixture
def path_fixture(request):
    return request.getfixturevalue(request.param)


def test__read_graphql_file__returns_content_of_file(single_file_schema):
    assert read_graphql_file(single_file_schema) == FIRST_SCHEMA


def test__walk_graphql_files__returns_graphql_files_from_directory(schemas_directory):
    assert sorted(f.name for f in walk_graphql_files(schemas_directory)) == sorted(
        [FIRST_FILENAME, SECOND_FILENAME]
    )


def test__walk_graphql_files__returns_graphql_files_from_nested_directory(
    schemas_nested_directories,
):
    assert sorted(
        f.name for f in walk_graphql_files(schemas_nested_directories)
    ) == sorted([FIRST_FILENAME, SECOND_FILENAME])


def test__load_schema_from_path__returns_schema_from_single_file(single_file_schema):
    assert load_schema_from_path(single_file_schema) == FIRST_SCHEMA


def test__load_schema_from_path__returns_schema_from_directory(schemas_directory):
    assert load_schema_from_path(schemas_directory) == "\n".join(
        [FIRST_SCHEMA, SECOND_SCHEMA]
    )


def test__load_schema_from_path__returns_schema_from_nested_directory(
    schemas_nested_directories,
):
    assert load_schema_from_path(schemas_nested_directories) == "\n".join(
        [FIRST_SCHEMA, SECOND_SCHEMA]
    )


@pytest.mark.parametrize(
    "path_fixture",
    ["single_file_schema", "schemas_directory", "schemas_nested_directories"],
    indirect=True,
)
def test__get_graphql_schema__returns_graphql_schema(mocker, path_fixture):
    mocker.patch(
        "graphql_sdk_gen.schema.settings",
        Settings(schema_path=path_fixture.as_posix()),
    )
    assert isinstance(get_graphql_schema(), GraphQLSchema)


def test__get_graphql_schema__raises_exception_with_incorrect_schema(
    mocker, incorrect_schema_file
):
    mocker.patch(
        "graphql_sdk_gen.schema.settings",
        Settings(schema_path=incorrect_schema_file.as_posix()),
    )
    with pytest.raises(GraphQLSyntaxError):
        get_graphql_schema()
