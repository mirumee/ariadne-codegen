from graphql import GraphQLSchema

from graphql_sdk_gen.generators.package import PackageGenerator


def test_generate_creates_directory_and_files(tmp_path):
    package_name = "test_graphql_cleint"
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


def test_generate_creates_files_with_correct_content(tmp_path):
    package_name = "test_graphql_cleint"
    generator = PackageGenerator(package_name, tmp_path.as_posix(), GraphQLSchema())

    generator.generate()

    package_path = tmp_path / package_name

    init_file_path = package_path / "__init__.py"
    with init_file_path.open() as init_file:
        init_content = init_file.read()
        assert "from .client import Client" in init_content
        assert '__all__ = ["Client"]' in init_content

    client_file_path = package_path / "client.py"
    with client_file_path.open() as client_file:
        client_content = client_file.read()
        assert "class Client:" in client_content
