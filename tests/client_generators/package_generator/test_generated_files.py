import ast
from textwrap import dedent

import pytest
from freezegun import freeze_time
from graphql import GraphQLSchema, parse

from ariadne_codegen.client_generators.arguments import ArgumentsGenerator
from ariadne_codegen.client_generators.client import ClientGenerator
from ariadne_codegen.client_generators.constants import (
    EXCEPTIONS_FILE_PATH,
    SOURCE_COMMENT,
    STABLE_COMMENT,
    TIMESTAMP_COMMENT,
)
from ariadne_codegen.client_generators.enums import EnumsGenerator
from ariadne_codegen.client_generators.fragments import FragmentsGenerator
from ariadne_codegen.client_generators.init_file import InitFileGenerator
from ariadne_codegen.client_generators.input_types import InputTypesGenerator
from ariadne_codegen.client_generators.package import PackageGenerator
from ariadne_codegen.client_generators.scalars import ScalarData
from ariadne_codegen.exceptions import ParsingError
from ariadne_codegen.settings import CommentsStrategy

from ...utils import get_class_def


def test_generate_creates_directory_and_files(
    tmp_path, schema, async_base_client_import
):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name=package_name,
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
    )

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


def test_generate_creates_files_with_correct_imports(
    tmp_path, async_base_client_import
):
    package_name = "test_graphql_client"
    schema = GraphQLSchema()
    generator = PackageGenerator(
        package_name=package_name,
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
    )

    generator.generate()

    package_path = tmp_path / package_name

    init_file_path = package_path / "__init__.py"
    with init_file_path.open() as init_file:
        init_content = init_file.read()
        assert "from .client import Client" in init_content
        assert "from .async_base_client import AsyncBaseClient" in init_content
        assert "from .base_model import BaseModel, Upload" in init_content
        expected_all = """
            __all__ = [
                "AsyncBaseClient",
                "BaseModel",
                "Client",
                "GraphQLClientError",
                "GraphQLClientGraphQLError",
                "GraphQLClientGraphQLMultiError",
                "GraphQLClientHttpError",
                "GraphQLClientInvalidResponseError",
                "Upload",
            ]
        """
        assert dedent(expected_all) in init_content

    client_file_path = package_path / "client.py"
    with client_file_path.open() as client_file:
        client_content = client_file.read()
        assert "class Client(AsyncBaseClient):" in client_content
        assert "from .async_base_client import AsyncBaseClient" in client_content


def test_generate_creates_files_with_types(tmp_path, schema, async_base_client_import):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name=package_name,
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
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


def test_generate_creates_file_with_query_types(
    tmp_path, schema, async_base_client_import
):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name=package_name,
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
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
        query_1: Optional["CustomQueryQuery1"] = Field(alias="query1")


    class CustomQueryQuery1(BaseModel):
        field_1: Optional[list[Optional[str]]] = Field(alias="field1")
        field_2: Optional["CustomQueryQuery1Field2"] = Field(alias="field2")
        field_3: CustomEnum = Field(alias="field3")


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


def test_generate_creates_multiple_query_types_files(
    tmp_path, schema, async_base_client_import
):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name=package_name,
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
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
    query1_file_path = package_path / "custom_query_1.py"
    assert query1_file_path.exists()
    assert query1_file_path.is_file()
    query2_file_path = package_path / "custom_query_2.py"
    assert query2_file_path.exists()
    assert query2_file_path.is_file()


def test_generate_copies_base_client_file(tmp_path, schema, async_base_client_import):
    base_client_file_content = """
    class TestBaseClient:
        pass
    """
    package_name = "test_graphql_client"
    base_client_file_path = tmp_path / "test_base_client.py"
    base_client_file_path.write_text(dedent(base_client_file_content))
    generator = PackageGenerator(
        package_name=package_name,
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
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


def test_generate_creates_client_with_valid_method_names(
    tmp_path, schema, async_base_client_import
):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name=package_name,
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        async_client=False,
    )
    query_str = """
    query From($id: ID!, $param: String) {
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
        parsed = ast.parse(client_content)
        class_def = get_class_def(parsed)
        function = [x for x in class_def.body if isinstance(x, ast.FunctionDef)][0]
        assert function.name == "from_"


def test_generate_with_conflicting_query_name_raises_parsing_error(
    tmp_path, schema, async_base_client_import
):
    generator = PackageGenerator(
        package_name="test_graphql_client",
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        input_types_module_name="input_types",
        convert_to_snake_case=True,
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
    tmp_path, schema, async_base_client_import
):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name=package_name,
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        async_client=True,
    )
    query_str = """
    query CustomQuery($val: CustomEnum!) {
        query3(val: $val) {
            id
        }
    }
    """

    expected_method_def = (
        "def custom_query(self, val: CustomEnum, **kwargs: Any) -> CustomQuery:"
    )
    expected_enum_import = f"from .{generator.enums_module_name} import CustomEnum"

    generator.add_operation(parse(query_str).definitions[0])
    generator.generate()

    client_file_path = tmp_path / package_name / "client.py"
    with client_file_path.open() as client_file:
        client_content = client_file.read()
        assert expected_method_def in client_content
        assert expected_enum_import in client_content


def test_generate_creates_client_file_with_gql_lambda_definition(
    tmp_path, schema, async_base_client_import
):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name=package_name,
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
    )

    generator.generate()

    client_file_path = tmp_path / package_name / "client.py"
    with client_file_path.open() as client_file:
        client_content = client_file.read()
        expected_gql_def = "def gql(q: str) -> str:\n    return q"
        assert expected_gql_def in client_content


@pytest.mark.parametrize(
    "strategy, expected_comment",
    [
        (CommentsStrategy.STABLE, STABLE_COMMENT),
        (
            CommentsStrategy.TIMESTAMP,
            TIMESTAMP_COMMENT.format("2022-01-01 12:00"),
        ),
    ],
)
@freeze_time("01.01.2022 12:00")
def test_generate_adds_comment_to_generated_files(
    tmp_path, schema, strategy, expected_comment, async_base_client_import
):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name=package_name,
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        comments_strategy=strategy,
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

    for file_name in files_names:
        file_path = package_path / file_name
        with file_path.open() as file_:
            content = file_.read()
            assert expected_comment in content


@pytest.mark.parametrize(
    "strategy", [CommentsStrategy.STABLE, CommentsStrategy.TIMESTAMP]
)
def test_generate_adds_comment_with_correct_source_to_generated_files(
    tmp_path, schema, async_base_client_import, strategy
):
    package_name = "test_graphql_client"
    schema_source = "schema_source.graphql"
    queries_source = "queries_source.graphql"
    generator = PackageGenerator(
        package_name=package_name,
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        comments_strategy=strategy,
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


@pytest.mark.parametrize(
    "strategy",
    [CommentsStrategy.NONE, CommentsStrategy.STABLE, CommentsStrategy.TIMESTAMP],
)
def test_generate_calls_get_file_comment_hook_for_every_file(
    tmp_path, schema, async_base_client_import, strategy, mocked_plugin_manager
):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name=package_name,
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        comments_strategy=strategy,
        plugin_manager=mocked_plugin_manager,
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

    assert len(list(tmp_path.joinpath(package_name).iterdir())) == len(
        mocked_plugin_manager.get_file_comment.mock_calls
    )


def test_generate_creates_result_types_from_operation_that_uses_fragment(
    tmp_path, schema, async_base_client_import
):
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
        query_1: Optional["CustomQueryQuery1"] = Field(alias="query1")


    class CustomQueryQuery1(TestFragment):
        field_3: CustomEnum = Field(alias="field3")
    """
    query_def, fragment_def = parse(query_str).definitions
    generator = PackageGenerator(
        package_name=package_name,
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(
            schema=schema, fragments_definitions={"TestFragment": fragment_def}
        ),
        fragments_definitions={"TestFragment": fragment_def},
    )

    generator.add_operation(query_def)
    generator.generate()

    result_types_file_path = tmp_path / package_name / "custom_query.py"
    with result_types_file_path.open() as result_types_file:
        result_types_content = result_types_file.read()
        assert dedent(expected_types) in result_types_content


def test_generate_returns_list_of_generated_files(
    tmp_path, schema, async_base_client_import
):
    fragments_definitions = {
        "TestFragment": parse("fragment TestFragment on CustomType { id }").definitions[
            0
        ]
    }
    generator = PackageGenerator(
        package_name="test_graphql_client",
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(
            schema=schema, fragments_definitions=fragments_definitions
        ),
        fragments_definitions=fragments_definitions,
        custom_scalars={"SCALARABC": ScalarData(type_="str", graphql_name="SCALARABC")},
    )
    query_str = """
    query CustomQuery {
        query2 {
            ...TestFragment
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
            EXCEPTIONS_FILE_PATH.name,
            f"{generator.input_types_module_name}.py",
            f"{generator.enums_module_name}.py",
            "custom_query.py",
            f"{generator.fragments_module_name}.py",
        ]
    )


def test_generate_copies_files_to_include(tmp_path, schema, async_base_client_import):
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
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(schema=schema),
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(schema=schema),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        files_to_include=[file1.as_posix(), file2.as_posix()],
    )
    generated_files = generator.generate()

    assert "file1.py" in generated_files
    package_path = tmp_path / "test_graphql_client"
    with package_path.joinpath("file1.py").open() as copied_file1:
        assert file1_content in copied_file1.read()
    with package_path.joinpath("file2.py").open() as copied_file2:
        assert file2_content in copied_file2.read()


def test_generate_creates_client_with_custom_scalars_imports(
    tmp_path, schema, async_base_client_import
):
    package_name = "test_graphql_client"
    custom_scalars = {
        "SCALARABC": ScalarData(type_=".abc.ScalarABC", graphql_name="SCALARABC")
    }
    generator = PackageGenerator(
        package_name=package_name,
        target_path=tmp_path.as_posix(),
        schema=schema,
        init_generator=InitFileGenerator(),
        client_generator=ClientGenerator(
            base_client_import=async_base_client_import,
            arguments_generator=ArgumentsGenerator(
                schema=schema, custom_scalars=custom_scalars
            ),
            custom_scalars=custom_scalars,
        ),
        enums_generator=EnumsGenerator(schema=schema),
        input_types_generator=InputTypesGenerator(
            schema=schema, custom_scalars=custom_scalars
        ),
        fragments_generator=FragmentsGenerator(schema=schema, fragments_definitions={}),
        custom_scalars=custom_scalars,
    )
    query_str = """
    query CustomQuery($id: ID!, $param: SCALARABC) {
        query1(id: $id, param: $param) {
            field1
        }
    }
    """

    generator.add_operation(parse(query_str).definitions[0])
    generator.generate()

    package_path = tmp_path / "test_graphql_client"
    with package_path.joinpath(
        f"{generator.client_file_name}.py"
    ).open() as client_file:
        assert "from .abc import ScalarABC" in client_file.read()
