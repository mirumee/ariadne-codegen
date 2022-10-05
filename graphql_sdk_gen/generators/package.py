import ast
from pathlib import Path

from graphql import GraphQLSchema, OperationDefinitionNode

from ..exceptions import ParsingError
from .arguments import ArgumentsGenerator
from .client import ClientGenerator
from .init_file import InitFileGenerator
from .query_types import QueryTypesGenerator
from .schema_types import SchemaTypesGenerator
from .utils import ast_to_str, str_to_snake_case


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
        self.schema_types_generator = SchemaTypesGenerator(schema)
        self.schema_types_module_name = "schema_types"

        self.query_types_files: dict[str, ast.Module] = {}

    def _create_init_file(self):
        init_file_path = self.package_path / "__init__.py"
        init_module = self.init_generator.generate()
        init_file_path.write_text(ast_to_str(init_module))

    def _create_client_file(self):
        client_file_path = self.package_path / "client.py"

        base_types = []
        for type_ in self.arguments_generator.used_types:
            if type_ in self.schema_types_generator.public_names:
                base_types.append(type_)
            else:
                raise ParsingError("Argument type not found in schema.")

        self.client_generator.add_import(
            names=base_types, from_=self.schema_types_module_name, level=1
        )
        client_module = self.client_generator.generate()
        client_file_path.write_text(ast_to_str(client_module))

        self.init_generator.add_import(
            names=[self.client_generator.name], from_="client", level=1
        )

    def _create_schema_types_file(self):
        types_module = self.schema_types_generator.generate()
        types_file_path = self.package_path / f"{self.schema_types_module_name}.py"
        types_file_path.write_text(ast_to_str(types_module))
        self.init_generator.add_import(
            self.schema_types_generator.public_names, self.schema_types_module_name, 1
        )

    def _create_query_types_files(self):
        for file_name, module in self.query_types_files.items():
            file_path = self.package_path / file_name
            file_path.write_text(ast_to_str(module))

    def generate(self):
        """Generate package with graphql client."""
        if not self.package_path.exists():
            self.package_path.mkdir()
        self._create_client_file()
        self._create_schema_types_file()
        self._create_query_types_files()
        self._create_init_file()

    def add_query(self, definition: OperationDefinitionNode):
        if not (name := definition.name):
            raise Exception

        query_name = name.value
        method_name = str_to_snake_case(name.value)
        module_name = method_name
        file_name = f"{module_name}.py"

        query_types_generator = QueryTypesGenerator(
            self.schema,
            self.schema_types_generator.fields,
            self.schema_types_generator.class_types,
            definition,
            self.schema_types_module_name,
        )
        self.query_types_files[file_name] = query_types_generator.generate()
        self.init_generator.add_import(
            query_types_generator.public_names, module_name, 1
        )

        arguments = self.arguments_generator.generate(definition.variable_definitions)
        self.client_generator.add_async_method(method_name, query_name, arguments)
        self.client_generator.add_import([query_name], module_name, 1)
