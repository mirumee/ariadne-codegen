from datetime import datetime
from textwrap import dedent, indent

import pytest
from freezegun import freeze_time
from graphql import GraphQLSchema, build_ast_schema, parse

from ariadne_codegen.exceptions import ParsingError
from ariadne_codegen.generators.constants import (
    COMMENT_DATETIME_FORMAT,
    SOURCE_COMMENT,
    TIMESTAMP_COMMENT,
)
from ariadne_codegen.generators.package import PackageGenerator

SCHEMA_STR = """
schema {
    query: Query
}

type Query {
    query1(
        id: ID!
    ): CustomType
    query2: [CustomType!]
    query3(val: CustomEnum!): [CustomType]
}

type CustomType {
    id: ID!
    field1: [String]
    field2: CustomType2
    field3: CustomEnum!
}

type CustomType2 {
    fieldb: Int
}

enum CustomEnum {
    VAL1
    VAL2
}

input CustomInput {
    value: Int!
}
"""


def test_generate_creates_directory_and_files(tmp_path):
    package_name = "test_graphql_client"
    generator = PackageGenerator(package_name, tmp_path.as_posix(), GraphQLSchema())

    generator.generate()

    package_path = tmp_path / package_name
    assert package_path.exists()
    assert package_path.is_dir()
    init_file_path = package_path / "__init__.py"
    assert init_file_path.exists()
    assert init_file_path.is_file()
    client_file_path = package_path / "client.py"
    assert client_file_path.exists()
    assert client_file_path.is_file()
    input_types_path = package_path / f"{generator.input_types_module_name}.py"
    assert input_types_path.exists()
    assert input_types_path.is_file()
    enums_path = package_path / f"{generator.enums_module_name}.py"
    assert enums_path.exists()
    assert enums_path.is_file()
    base_client_path = package_path / generator.base_client_file_path.name
    assert base_client_path.exists()
    assert base_client_path.is_file()
    base_model_path = package_path / "base_model.py"
    assert base_model_path.exists()
    assert base_model_path.is_file()


def test_generate_creates_files_with_correct_imports(tmp_path):
    package_name = "test_graphql_client"
    generator = PackageGenerator(package_name, tmp_path.as_posix(), GraphQLSchema())

    generator.generate()

    package_path = tmp_path / package_name

    init_file_path = package_path / "__init__.py"
    with init_file_path.open() as init_file:
        init_content = init_file.read()
        assert "from .client import Client" in init_content
        assert "from .async_base_client import AsyncBaseClient" in init_content
        assert "from .base_model import BaseModel" in init_content
        expected_all = """
            __all__ = [
                "AsyncBaseClient",
                "BaseModel",
                "Client",
                "GraphQLClientError",
                "GraphQLClientGraphQLError",
                "GraphQLClientGraphQLMultiError",
                "GraphQLClientHttpError",
                "GraphQlClientInvalidResponseError",
            ]
        """
        assert dedent(expected_all) in init_content

    client_file_path = package_path / "client.py"
    with client_file_path.open() as client_file:
        client_content = client_file.read()
        assert "class Client(AsyncBaseClient):" in client_content
        assert "from .async_base_client import AsyncBaseClient" in client_content


def test_generate_creates_files_with_types(tmp_path):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name, tmp_path.as_posix(), build_ast_schema(parse(SCHEMA_STR))
    )
    expected_input_types = """
    class CustomInput(BaseModel):
        value: int
    """
    expected_enums = """
    class CustomEnum(str, Enum):
        VAL1 = "VAL1"
        VAL2 = "VAL2"
    """

    generator.generate()

    input_types_file_path = (
        tmp_path / package_name / f"{generator.input_types_module_name}.py"
    )
    with input_types_file_path.open() as input_types_file:
        input_types_content = input_types_file.read()
        assert dedent(expected_input_types) in input_types_content

    enums_file_path = tmp_path / package_name / f"{generator.enums_module_name}.py"
    with enums_file_path.open() as enums_file:
        enums_content = enums_file.read()
        assert dedent(expected_enums) in enums_content


def test_generate_creates_file_with_query_types(tmp_path):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name, tmp_path.as_posix(), build_ast_schema(parse(SCHEMA_STR))
    )
    query_str = """
    query CustomQuery($id: ID!, $param: String) {
        query1(id: $id) {
            field1
            field2 {
                fieldb
            }
            field3
        }
    }
    """
    expected_query_types = """
    class CustomQuery(BaseModel):
        query1: Optional["CustomQueryQuery1"]


    class CustomQueryQuery1(BaseModel):
        field1: Optional[List[Optional[str]]]
        field2: Optional["CustomQueryQuery1Field2"]
        field3: CustomEnum


    class CustomQueryQuery1Field2(BaseModel):
        fieldb: Optional[int]
    """

    generator.add_operation(parse(query_str).definitions[0])
    generator.generate()

    query_types_file_path = tmp_path / package_name / "custom_query.py"
    with query_types_file_path.open() as query_types_file:
        query_types_content = query_types_file.read()
        assert dedent(expected_query_types) in query_types_content
        assert (
            f"from .{generator.enums_module_name} import CustomEnum"
            in query_types_content
        )


def test_generate_creates_multiple_query_types_files(tmp_path):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name, tmp_path.as_posix(), build_ast_schema(parse(SCHEMA_STR))
    )
    query_str = """
    query CustomQuery1 {
        query2 {
            id
        }
    }

    query CustomQuery2 {
        query2 {
            id
        }
    }
    """

    for definition in parse(query_str).definitions:
        generator.add_operation(definition)
    generator.generate()

    package_path = tmp_path / package_name
    query1_file_path = package_path / "custom_query1.py"
    assert query1_file_path.exists()
    assert query1_file_path.is_file()
    query2_file_path = package_path / "custom_query2.py"
    assert query2_file_path.exists()
    assert query2_file_path.is_file()


def test_generate_copies_base_client_file(tmp_path):
    base_client_file_content = """
    class TestBaseClient:
        pass
    """
    package_name = "test_graphql_client"
    base_client_file_path = tmp_path / "test_base_client.py"
    base_client_file_path.write_text(dedent(base_client_file_content))
    generator = PackageGenerator(
        package_name,
        tmp_path.as_posix(),
        build_ast_schema(parse(SCHEMA_STR)),
        base_client_name="TestBaseClient",
        base_client_file_path=base_client_file_path.as_posix(),
    )

    generator.generate()

    copied_file_path = tmp_path / package_name / "test_base_client.py"
    assert copied_file_path.exists()
    assert copied_file_path.is_file()
    with copied_file_path.open() as copied_file:
        copied_content = copied_file.read()
        assert dedent(base_client_file_content) in dedent(copied_content)


def test_generate_creates_client_with_correctly_implemented_async_method(tmp_path):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name,
        tmp_path.as_posix(),
        build_ast_schema(parse(SCHEMA_STR)),
        async_client=True,
    )
    query_str = """
    query CustomQuery($id: ID!, $param: String) {
        query1(id: $id) {
            field1
            field2 {
                fieldb
            }
            field3
        }
    }
    """

    generator.add_operation(parse(query_str).definitions[0])
    generator.generate()

    client_file_path = tmp_path / package_name / "client.py"
    with client_file_path.open() as client_file:
        client_content = client_file.read()

        expected_method_def = '''
        async def custom_query(self, id: str, param: Optional[str]) -> CustomQuery:
            query = gql(
                """
                query CustomQuery($id: ID!, $param: String) {
                  query1(id: $id) {
                    field1
                    field2 {
                      fieldb
                    }
                    field3
                  }
                }
                """
            )
            variables: dict = {"id": id, "param": param}
            response = await self.execute(query=query, variables=variables)
            data = self.get_data(response)
            return CustomQuery.parse_obj(data)
        '''
        assert indent(dedent(expected_method_def), "    ") in client_content
        assert "from .custom_query import CustomQuery" in client_content


def test_generate_with_conflicting_query_name_raises_parsing_error(tmp_path):
    generator = PackageGenerator(
        "test_graphql_client",
        tmp_path.as_posix(),
        build_ast_schema(parse(SCHEMA_STR)),
        input_types_module_name="input_types",
    )
    query_str = """
    query InputTypes {
        query2 {
            id
        }
    }
    """
    generator.add_operation(parse(query_str).definitions[0])

    with pytest.raises(ParsingError):
        generator.generate()


def test_generate_with_enum_as_query_argument_generates_client_with_correct_method(
    tmp_path,
):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name,
        tmp_path.as_posix(),
        build_ast_schema(parse(SCHEMA_STR)),
        async_client=True,
    )
    query_str = """
    query CustomQuery($val: CustomEnum!) {
        query3(val: $val) {
            id
        }
    }
    """

    expected_method_def = "def custom_query(self, val: CustomEnum) -> CustomQuery:"
    expected_enum_import = f"from .{generator.enums_module_name} import CustomEnum"

    generator.add_operation(parse(query_str).definitions[0])
    generator.generate()

    client_file_path = tmp_path / package_name / "client.py"
    with client_file_path.open() as client_file:
        client_content = client_file.read()
        assert expected_method_def in client_content
        assert expected_enum_import in client_content


def test_generate_creates_client_file_with_gql_lambda_definition(tmp_path):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name, tmp_path.as_posix(), build_ast_schema(parse(SCHEMA_STR))
    )

    generator.generate()

    client_file_path = tmp_path / package_name / "client.py"
    with client_file_path.open() as client_file:
        client_content = client_file.read()
        expected_gql_def = "def gql(q: str) -> str:\n    return q"
        assert expected_gql_def in client_content


@freeze_time("01.12.2022 12:00")
def test_generate_adds_comment_with_timestamp_to_generated_files(tmp_path):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name,
        tmp_path.as_posix(),
        build_ast_schema(parse(SCHEMA_STR)),
        include_comments=True,
    )
    query_str = """
    query CustomQuery($val: CustomEnum!) {
        query3(val: $val) {
            id
        }
    }
    """
    generator.add_operation(parse(query_str).definitions[0])
    generator.generate()

    package_path = tmp_path / package_name
    files_names = [
        "__init__.py",
        generator.base_client_file_path.name,
        f"{generator.enums_module_name}.py",
        f"{generator.input_types_module_name}.py",
        "custom_query.py",
    ]
    expected_comment = TIMESTAMP_COMMENT.format(
        datetime.now().strftime(COMMENT_DATETIME_FORMAT)
    )
    for file_name in files_names:
        file_path = package_path / file_name
        with file_path.open() as file_:
            content = file_.read()
            assert expected_comment in content


def test_generate_adds_comment_with_correct_source_to_generated_files(tmp_path):
    package_name = "test_graphql_client"
    schema_source = "schema_source.graphql"
    queries_source = "queries_source.graphql"
    generator = PackageGenerator(
        package_name,
        tmp_path.as_posix(),
        build_ast_schema(parse(SCHEMA_STR)),
        include_comments=True,
        schema_source=schema_source,
        queries_source=queries_source,
    )
    query_str = """
    query CustomQuery($val: CustomEnum!) {
        query3(val: $val) {
            id
        }
    }
    """
    generator.add_operation(parse(query_str).definitions[0])
    generator.generate()

    package_path = tmp_path / package_name

    schema_source_files_names = [
        f"{generator.enums_module_name}.py",
        f"{generator.input_types_module_name}.py",
    ]
    expected_schema_source_comment = SOURCE_COMMENT.format(schema_source)
    for file_name in schema_source_files_names:
        file_path = package_path / file_name
        with file_path.open() as file_:
            content = file_.read()
            assert expected_schema_source_comment in content

    expected_queries_source_comment = SOURCE_COMMENT.format(queries_source)
    with package_path.joinpath("custom_query.py").open() as query_types_file:
        content = query_types_file.read()
        assert expected_queries_source_comment in content


def test_generate_creates_result_types_from_operation_that_uses_fragment(tmp_path):
    package_name = "test_graphql_client"
    query_str = """
    query CustomQuery($id: ID!) {
        query1(id: $id) {
            ...TestFragment
            field3
        }
    }

    fragment TestFragment on CustomType {
        field1
        field2 {
            fieldb
        }
    }
    """
    expected_types = """
    class CustomQuery(BaseModel):
        query1: Optional["CustomQueryQuery1"]


    class CustomQueryQuery1(BaseModel):
        field1: Optional[List[Optional[str]]]
        field2: Optional["CustomQueryQuery1Field2"]
        field3: CustomEnum


    class CustomQueryQuery1Field2(BaseModel):
        fieldb: Optional[int]
    """
    query_def, fragment_def = parse(query_str).definitions
    generator = PackageGenerator(
        package_name,
        tmp_path.as_posix(),
        build_ast_schema(parse(SCHEMA_STR)),
        fragments=[fragment_def],
    )

    generator.add_operation(query_def)
    generator.generate()

    result_types_file_path = tmp_path / package_name / "custom_query.py"
    with result_types_file_path.open() as result_types_file:
        result_types_content = result_types_file.read()
        assert dedent(expected_types) in result_types_content


def test_generate_returns_list_of_generated_files(tmp_path):
    generator = PackageGenerator(
        "test_graphql_client",
        tmp_path.as_posix(),
        build_ast_schema(parse(SCHEMA_STR)),
    )
    query_str = """
    query CustomQuery {
        query2 {
            id
        }
    }
    """
    generator.add_operation(parse(query_str).definitions[0])

    generated_files = generator.generate()

    assert sorted(generated_files) == sorted(
        [
            "__init__.py",
            generator.base_client_file_path.name,
            "base_model.py",
            f"{generator.client_file_name}.py",
            generator.exceptions_file_path.name,
            f"{generator.input_types_module_name}.py",
            f"{generator.enums_module_name}.py",
            "custom_query.py",
        ]
    )


def test_generate_copies_files_to_include(tmp_path):
    file1 = tmp_path / "file1.py"
    file1_content = "class TestBaseClass:\n    pass"
    file1.write_text(file1_content)

    file2_dir = tmp_path / "dir"
    file2_dir.mkdir()
    file2 = file2_dir / "file2.py"
    file2_content = "class TestBaseClass2:\n    pass"
    file2.write_text(file2_content)

    generator = PackageGenerator(
        package_name="test_graphql_client",
        target_path=tmp_path.as_posix(),
        schema=build_ast_schema(parse(SCHEMA_STR)),
        files_to_include=[file1.as_posix(), file2.as_posix()],
    )
    generated_files = generator.generate()

    assert "file1.py" in generated_files
    package_path = tmp_path / "test_graphql_client"
    with package_path.joinpath("file1.py").open() as copied_file1:
        assert file1_content in copied_file1.read()
    with package_path.joinpath("file2.py").open() as copied_file2:
        assert file2_content in copied_file2.read()
