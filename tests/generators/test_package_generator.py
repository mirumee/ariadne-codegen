from textwrap import dedent, indent

from graphql import GraphQLSchema, build_ast_schema, parse

from graphql_sdk_gen.generators.package import PackageGenerator

SCHEMA_STR = """
schema {
    query: Query

}

type Query {
    query1(
        id: ID!
    ): CustomType
    query2: [CustomType!]
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
    schema_types_path = package_path / f"{generator.schema_types_module_name}.py"
    assert schema_types_path.exists()
    assert schema_types_path.is_file()


def test_generate_creates_files_with_correct_content(tmp_path):
    package_name = "test_graphql_client"
    generator = PackageGenerator(package_name, tmp_path.as_posix(), GraphQLSchema())

    generator.generate()

    package_path = tmp_path / package_name

    init_file_path = package_path / "__init__.py"
    with init_file_path.open() as init_file:
        init_content = init_file.read()
        assert "from .client import Client" in init_content
        assert "from .base_client import BaseClient" in init_content
        assert '__all__ = ["BaseClient", "Client"]' in init_content

    client_file_path = package_path / "client.py"
    with client_file_path.open() as client_file:
        client_content = client_file.read()
        assert "class Client(BaseClient):" in client_content
        assert "from .base_client import BaseClient" in client_content


def test_generate_creates_files_with_types(tmp_path):
    package_name = "test_graphql_client"
    generator = PackageGenerator(
        package_name, tmp_path.as_posix(), build_ast_schema(parse(SCHEMA_STR))
    )
    expected_schema_types = """
    class CustomType(BaseModel):
        id: str
        field1: Optional[list[Optional[str]]]
        field2: Optional["CustomType2"]
        field3: "CustomEnum"


    class CustomType2(BaseModel):
        fieldb: Optional[int]


    class CustomEnum(str, Enum):
        VAL1 = "VAL1"
        VAL2 = "VAL2"
    """

    generator.generate()

    types_file_path = (
        tmp_path / package_name / f"{generator.schema_types_module_name}.py"
    )
    with types_file_path.open() as type_file:
        types_content = type_file.read()
        assert dedent(expected_schema_types) in types_content


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
    class CustomQueryCustomType2(BaseModel):
        fieldb: Optional[int]


    class CustomQueryCustomType(BaseModel):
        field1: Optional[list[Optional[str]]]
        field2: Optional["CustomQueryCustomType2"]
        field3: "CustomEnum"


    class CustomQuery(BaseModel):
        query1: Optional["CustomQueryCustomType"]
    """

    generator.add_query(parse(query_str).definitions[0])
    generator.generate()

    query_types_file_path = tmp_path / package_name / "custom_query.py"
    with query_types_file_path.open() as query_types_file:
        query_types_content = query_types_file.read()
        assert dedent(expected_query_types) in query_types_content
        assert (
            f"from .{generator.schema_types_module_name} import CustomEnum"
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
        generator.add_query(definition)
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
        assert dedent(copied_content) == dedent(base_client_file_content)


def test_generate_creates_client_with_correctly_implemented_method(tmp_path):
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

    generator.add_query(parse(query_str).definitions[0])
    generator.generate()

    client_file_path = tmp_path / package_name / "client.py"
    with client_file_path.open() as client_file:
        client_content = client_file.read()

        expected_method_def = """
        async def custom_query(self, id: str, param: Optional[str]) -> CustomQuery:
            query = (
                "query CustomQuery($id: ID!, $param: String) {\\n"
                "  query1(id: $id) {\\n"
                "    field1\\n"
                "    field2 {\\n"
                "      fieldb\\n"
                "    }\\n"
                "    field3\\n"
                "  }\\n"
                "}\\n"
            )
            variables: dict = {"id": id, "param": param}
            response = await self.execute(query=query, variables=variables)
            return CustomQuery.parse_obj(response.json().get("data", {}))
        """
        assert indent(dedent(expected_method_def), "    ") in client_content
        assert "from .custom_query import CustomQuery" in client_content
