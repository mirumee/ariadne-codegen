from pathlib import Path

from graphql import OperationDefinitionNode, GraphQLSchema

from .client import ClientGenerator
from .init_file import InitFileGenerator
from .utils import ast_to_str, to_snake_case
from .arguments import ArgumentsGenerator
from .base_types import BaseTypesGenerator
from .query_types import QueryTypesGenerator


class PackageGenerator:
    def __init__(
        self, package_name: str, target_path: str, schema: GraphQLSchema
    ) -> None:
        self.package_name = package_name
        self.target_path = target_path
        self.schema = schema
        self.package_path = Path(target_path) / package_name

        self.init_generator = InitFileGenerator()
        self.client_generator = ClientGenerator()
        self.arguments_generator = ArgumentsGenerator()
        self.base_types_generator = BaseTypesGenerator(schema)
        self.query_types_generator = QueryTypesGenerator(
            schema, self.base_types_generator.types_definitions
        )

    def _create_init_file(self):
        init_file_path = self.package_path / "__init__.py"
        init_module = self.init_generator.generate()
        init_file_path.write_text(ast_to_str(init_module))

    def _create_client_file(self):
        client_file_path = self.package_path / "client.py"
        self.client_generator.add_import(names=["Optional"], from_="typing")

        base_types = []
        for type_ in self.arguments_generator.non_scalar_types:
            if type_ in self.base_types_generator.types_definitions:
                base_types.append(type_)
            else:
                raise Exception

        self.client_generator.add_import(names=base_types, from_="types", level=1)
        client_module = self.client_generator.generate()
        client_file_path.write_text(ast_to_str(client_module))

        self.init_generator.add_import(
            names=[self.client_generator.name], from_="client", level=1
        )

    def _create_types_files(self):
        types_module, types_filename = self.base_types_generator.generate()
        types_file_path = self.package_path / types_filename
        types_file_path.write_text(ast_to_str(types_module))

    def generate(self):
        """Generate package with graphql client."""
        if not self.package_path.exists():
            self.package_path.mkdir()
        self._create_client_file()
        self._create_init_file()
        self._create_types_files()

    def add_query(self, definition: OperationDefinitionNode):
        if not self.package_path.exists():
            self.package_path.mkdir()
        if not (name := definition.name):
            raise Exception
        method_name = to_snake_case(name.value)
        arguments = self.arguments_generator.generate(definition.variable_definitions)
        types_module = self.query_types_generator.generate(definition)
        types_file_path = self.package_path / f"{method_name}.py"
        types_file_path.write_text(ast_to_str(types_module))
        self.client_generator.add_async_method(method_name, name.value, arguments)
