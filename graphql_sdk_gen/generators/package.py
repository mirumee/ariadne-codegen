import ast
from datetime import datetime
from pathlib import Path
from typing import Optional

from graphql import FragmentDefinitionNode, GraphQLSchema, OperationDefinitionNode

from ..exceptions import ParsingError
from .arguments import ArgumentsGenerator
from .client import ClientGenerator
from .codegen import generate_import_from
from .constants import (
    BASE_MODEL_CLASS_NAME,
    COMMENT_DATETIME_FORMAT,
    SOURCE_COMMENT,
    TIMESTAMP_COMMENT,
)
from .init_file import InitFileGenerator
from .result_types import ResultTypesGenerator
from .schema_types import SchemaTypesGenerator
from .utils import ast_to_str, str_to_pascal_case, str_to_snake_case


class PackageGenerator:
    def __init__(
        self,
        package_name: str,
        target_path: str,
        schema: GraphQLSchema,
        client_name: str = "Client",
        client_file_name: str = "client",
        base_client_name: str = "AsyncBaseClient",
        base_client_file_path: Optional[str] = None,
        schema_types_module_name: str = "schema_types",
        enums_module_name: str = "enums",
        input_types_module_name: str = "input_types",
        include_comments: bool = True,
        queries_source: str = "",
        schema_source: str = "",
        convert_to_snake_case: bool = True,
        async_client: bool = True,
        fragments: Optional[list[FragmentDefinitionNode]] = None,
        init_generator: Optional[InitFileGenerator] = None,
        client_generator: Optional[ClientGenerator] = None,
        arguments_generator: Optional[ArgumentsGenerator] = None,
        schema_types_generator: Optional[SchemaTypesGenerator] = None,
        files_to_include: Optional[list[str]] = None,
    ) -> None:
        self.package_name = package_name
        self.target_path = target_path
        self.schema = schema
        self.package_path = Path(target_path) / package_name
        self.client_name = client_name
        self.base_client_name = base_client_name

        self.base_model_file_path = Path(__file__).parent / "base_model.py"
        self.base_model_import = generate_import_from(
            [BASE_MODEL_CLASS_NAME], self.base_model_file_path.stem, 1
        )

        self.files_to_include = (
            [Path(f) for f in files_to_include] if files_to_include else []
        )

        self.schema_types_module_name = schema_types_module_name
        self.enums_module_name = enums_module_name
        self.input_types_module_name = input_types_module_name
        self.client_file_name = client_file_name

        self.include_comments = include_comments
        self.queries_source = queries_source
        self.schema_source = schema_source
        self.convert_to_snake_case = convert_to_snake_case
        self.async_client = async_client

        self.init_generator = init_generator if init_generator else InitFileGenerator()
        self.client_generator = (
            client_generator
            if client_generator
            else ClientGenerator(self.client_name, self.base_client_name)
        )
        self.arguments_generator = (
            arguments_generator
            if arguments_generator
            else ArgumentsGenerator(self.convert_to_snake_case)
        )
        self.schema_types_generator = (
            schema_types_generator
            if schema_types_generator
            else SchemaTypesGenerator(
                schema, self.convert_to_snake_case, self.base_model_import
            )
        )

        if base_client_file_path:
            self.base_client_file_path = Path(base_client_file_path)
        else:
            if self.async_client:
                self.base_client_file_path = Path(__file__).parent.joinpath(
                    "async_base_client.py"
                )
            else:
                self.base_client_file_path = Path(__file__).parent.joinpath(
                    "base_client.py"
                )

        self.fragments_definitions = {f.name.value: f for f in fragments or []}

        self.result_types_files: dict[str, ast.Module] = {}
        self.generated_files: list[str] = []

    def generate(self) -> list[str]:
        """Generate package with graphql client."""
        self._validate_unique_file_names()
        if not self.package_path.exists():
            self.package_path.mkdir()
        self._generate_client()
        self._generate_schema_types()
        self._generate_result_types()
        self._copy_files()
        self._generate_init()

        return sorted(self.generated_files)

    def add_operation(self, definition: OperationDefinitionNode):
        if not (name := definition.name):
            raise ParsingError("Query without name.")

        return_type_name = str_to_pascal_case(name.value)
        method_name = str_to_snake_case(name.value)
        module_name = method_name
        file_name = f"{module_name}.py"

        query_types_generator = ResultTypesGenerator(
            schema=self.schema,
            operation_definition=definition,
            enums_module_name=self.enums_module_name,
            fragments_definitions=self.fragments_definitions,
            base_model_import=self.base_model_import,
            convert_to_snake_case=self.convert_to_snake_case,
        )
        self.result_types_files[file_name] = query_types_generator.generate()
        operation_str = query_types_generator.get_operation_as_str()
        self.init_generator.add_import(
            query_types_generator.get_generated_public_names(), module_name, 1
        )

        arguments, arguments_dict = self.arguments_generator.generate(
            definition.variable_definitions
        )
        self.client_generator.add_method(
            name=method_name,
            return_type=return_type_name,
            arguments=arguments,
            arguments_dict=arguments_dict,
            operation_str=operation_str,
            async_=self.async_client,
        )
        self.client_generator.add_import([return_type_name], module_name, 1)

    def _validate_unique_file_names(self):
        file_names = (
            [
                f"{self.client_file_name}.py",
                self.base_client_file_path.name,
                self.base_model_file_path.name,
                f"{self.schema_types_module_name}.py",
                f"{self.enums_module_name}.py",
                f"{self.input_types_module_name}.py",
            ]
            + list(self.result_types_files.keys())
            + [f.name for f in self.files_to_include]
        )

        if len(file_names) != len(set(file_names)):
            seen = set()
            duplicated_files = {n for n in file_names if n in seen or seen.add(n)}
            raise ParsingError(f"Duplicated file names: {',' .join(duplicated_files)}")

    def _generate_client(self):
        client_file_path = self.package_path / f"{self.client_file_name}.py"

        input_types = []
        enums = []
        for type_ in self.arguments_generator.used_types:
            if type_ in self.schema_types_generator.input_types:
                input_types.append(type_)
            elif type_ in self.schema_types_generator.enums:
                enums.append(type_)
            else:
                raise ParsingError(f"Argument type {type_} not found in schema.")

        self.client_generator.add_import(
            names=input_types, from_=self.input_types_module_name, level=1
        )
        self.client_generator.add_import(
            names=enums, from_=self.enums_module_name, level=1
        )

        self.client_generator.add_import(
            names=[self.base_client_name],
            from_=self.base_client_file_path.stem,
            level=1,
        )

        client_module = self.client_generator.generate()
        code = self._proccess_generated_code(
            ast_to_str(client_module), self.queries_source
        )
        client_file_path.write_text(code)
        self.generated_files.append(client_file_path.name)

        self.init_generator.add_import(
            names=[self.client_generator.name], from_=self.client_file_name, level=1
        )

    def _proccess_generated_code(self, code: str, source: str = "") -> str:
        if self.include_comments:
            comments = [
                TIMESTAMP_COMMENT.format(
                    datetime.now().strftime(COMMENT_DATETIME_FORMAT)
                )
            ]
            if source:
                comments.append(SOURCE_COMMENT.format(source))
            return "".join(comments) + "\n" + code

        return code

    def _generate_schema_types(self):
        (
            enums_module,
            input_types_module,
            schema_types_module,
        ) = self.schema_types_generator.generate()

        schema_types_file_path = (
            self.package_path / f"{self.schema_types_module_name}.py"
        )
        schema_types_code = self._proccess_generated_code(
            ast_to_str(schema_types_module), self.schema_source
        )
        schema_types_file_path.write_text(schema_types_code)
        self.generated_files.append(schema_types_file_path.name)
        self.init_generator.add_import(
            self.schema_types_generator.schema_types, self.schema_types_module_name, 1
        )

        enums_file_path = self.package_path / f"{self.enums_module_name}.py"
        enums_code = self._proccess_generated_code(
            ast_to_str(enums_module), self.schema_source
        )
        enums_file_path.write_text(enums_code)
        self.generated_files.append(enums_file_path.name)
        self.init_generator.add_import(
            self.schema_types_generator.enums, self.enums_module_name, 1
        )

        input_types_file_path = self.package_path / f"{self.input_types_module_name}.py"
        input_types_code = self._proccess_generated_code(
            ast_to_str(input_types_module), self.schema_source
        )
        input_types_file_path.write_text(input_types_code)
        self.generated_files.append(input_types_file_path.name)
        self.init_generator.add_import(
            self.schema_types_generator.input_types, self.input_types_module_name, 1
        )

    def _generate_result_types(self):
        for file_name, module in self.result_types_files.items():
            file_path = self.package_path / file_name
            code = self._proccess_generated_code(
                ast_to_str(module), self.queries_source
            )
            file_path.write_text(code)
            self.generated_files.append(file_path.name)

    def _copy_files(self):
        for source_path in self.files_to_include + [
            self.base_client_file_path,
            self.base_model_file_path,
        ]:
            code = self._proccess_generated_code(source_path.read_text())
            target_path = self.package_path / source_path.name
            target_path.write_text(code)
            self.generated_files.append(target_path.name)

        self.init_generator.add_import(
            names=[self.base_client_name],
            from_=self.base_client_file_path.stem,
            level=1,
        )
        self.init_generator.add_import(
            names=[BASE_MODEL_CLASS_NAME],
            from_=self.base_model_file_path.stem,
            level=1,
        )

    def _generate_init(self):
        init_file_path = self.package_path / "__init__.py"
        init_module = self.init_generator.generate()
        code = self._proccess_generated_code(ast_to_str(init_module, False))
        init_file_path.write_text(code)
        self.generated_files.append(init_file_path.name)
