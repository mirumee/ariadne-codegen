import ast
from datetime import datetime
from pathlib import Path
from typing import Optional

from graphql import (
    FragmentDefinitionNode,
    GraphQLEnumType,
    GraphQLInputObjectType,
    GraphQLSchema,
    OperationDefinitionNode,
)

from ..exceptions import ParsingError
from .arguments import ArgumentsGenerator
from .client import ClientGenerator
from .codegen import generate_import_from
from .constants import (
    BASE_MODEL_CLASS_NAME,
    COMMENT_DATETIME_FORMAT,
    DEFAULT_ASYNC_BASE_CLIENT_PATH,
    DEFAULT_BASE_CLIENT_PATH,
    GRAPHQL_CLIENT_EXCEPTIONS_NAMES,
    SOURCE_COMMENT,
    TIMESTAMP_COMMENT,
)
from .enums import EnumsGenerator
from .init_file import InitFileGenerator
from .input_types import InputTypesGenerator
from .result_types import ResultTypesGenerator
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
        enums_generator: Optional[EnumsGenerator] = None,
        input_types_generator: Optional[InputTypesGenerator] = None,
        files_to_include: Optional[list[str]] = None,
    ) -> None:
        self.package_name = package_name
        self.target_path = target_path
        self.schema = schema
        self.package_path = Path(target_path) / package_name
        self.client_name = client_name
        self.base_client_name = base_client_name

        self.base_model_file_path = (
            Path(__file__).parent / "dependencies" / "base_model.py"
        )
        self.base_model_import = generate_import_from(
            [BASE_MODEL_CLASS_NAME], self.base_model_file_path.stem, 1
        )
        self.exceptions_file_path = (
            Path(__file__).parent / "dependencies" / "exceptions.py"
        )

        self.files_to_include = (
            [Path(f) for f in files_to_include] if files_to_include else []
        )

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
            else ClientGenerator(
                name=self.client_name, base_client=self.base_client_name
            )
        )
        self.arguments_generator = (
            arguments_generator
            if arguments_generator
            else ArgumentsGenerator(convert_to_snake_case=self.convert_to_snake_case)
        )
        self.input_types_generator = (
            input_types_generator
            if input_types_generator
            else InputTypesGenerator(
                schema=self.schema,
                enums_module=self.enums_module_name,
                convert_to_snake_case=self.convert_to_snake_case,
                base_model_import=self.base_model_import,
            )
        )
        self.enums_generator = (
            enums_generator if enums_generator else EnumsGenerator(schema=self.schema)
        )

        if base_client_file_path:
            self.base_client_file_path = Path(base_client_file_path)
        else:
            if self.async_client:
                self.base_client_file_path = DEFAULT_ASYNC_BASE_CLIENT_PATH
            else:
                self.base_client_file_path = DEFAULT_BASE_CLIENT_PATH

        self.fragments_definitions = {f.name.value: f for f in fragments or []}

        self.result_types_files: dict[str, ast.Module] = {}
        self.generated_files: list[str] = []
        self.include_exceptions_file = self._include_exceptions()

    def generate(self) -> list[str]:
        """Generate package with graphql client."""
        self._validate_unique_file_names()
        if not self.package_path.exists():
            self.package_path.mkdir()
        self._generate_client()
        self._generate_enums()
        self._generate_input_types()
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

    def _include_exceptions(self):
        return self.base_client_file_path in (
            DEFAULT_ASYNC_BASE_CLIENT_PATH,
            DEFAULT_BASE_CLIENT_PATH,
        )

    def _validate_unique_file_names(self):
        file_names = (
            [
                f"{self.client_file_name}.py",
                self.base_client_file_path.name,
                self.base_model_file_path.name,
                f"{self.enums_module_name}.py",
                f"{self.input_types_module_name}.py",
            ]
            + list(self.result_types_files.keys())
            + [f.name for f in self.files_to_include]
        )
        if self.include_exceptions_file:
            file_names.append(self.exceptions_file_path.name)

        if len(file_names) != len(set(file_names)):
            seen = set()
            duplicated_files = {n for n in file_names if n in seen or seen.add(n)}
            raise ParsingError(f"Duplicated file names: {',' .join(duplicated_files)}")

    def _generate_client(self):
        client_file_path = self.package_path / f"{self.client_file_name}.py"

        input_types = []
        enums = []
        for type_ in self.arguments_generator.used_types:
            if isinstance(self.schema.type_map[type_], GraphQLInputObjectType):
                input_types.append(type_)
            elif isinstance(self.schema.type_map[type_], GraphQLEnumType):
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

    def _generate_enums(self):
        module = self.enums_generator.generate()
        code = self._proccess_generated_code(ast_to_str(module), self.schema_source)
        enums_file_path = self.package_path / f"{self.enums_module_name}.py"
        enums_file_path.write_text(code)
        self.generated_files.append(enums_file_path.name)
        self.init_generator.add_import(
            self.enums_generator.get_generated_public_names(), self.enums_module_name, 1
        )

    def _generate_input_types(self):
        module = self.input_types_generator.generate()
        input_types_file_path = self.package_path / f"{self.input_types_module_name}.py"
        input_types_code = self._proccess_generated_code(
            ast_to_str(module), self.schema_source
        )
        input_types_file_path.write_text(input_types_code)
        self.generated_files.append(input_types_file_path.name)
        self.init_generator.add_import(
            self.input_types_generator.get_generated_public_names(),
            self.input_types_module_name,
            1,
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
        files_to_copy = self.files_to_include + [
            self.base_client_file_path,
            self.base_model_file_path,
        ]
        if self.include_exceptions_file:
            files_to_copy.append(self.exceptions_file_path)
            self.init_generator.add_import(
                names=GRAPHQL_CLIENT_EXCEPTIONS_NAMES,
                from_=self.exceptions_file_path.stem,
                level=1,
            )
        for source_path in files_to_copy:
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
