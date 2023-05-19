import ast
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

from graphql import FragmentDefinitionNode, GraphQLSchema, OperationDefinitionNode

from ..codegen import generate_import_from
from ..exceptions import ParsingError
from ..plugins.manager import PluginManager
from ..utils import ast_to_str, process_name, str_to_pascal_case
from .arguments import ArgumentsGenerator
from .client import ClientGenerator
from .constants import (
    BASE_MODEL_CLASS_NAME,
    COMMENT_DATETIME_FORMAT,
    DEFAULT_ASYNC_BASE_CLIENT_PATH,
    DEFAULT_BASE_CLIENT_PATH,
    GRAPHQL_CLIENT_EXCEPTIONS_NAMES,
    SOURCE_COMMENT,
    TIMESTAMP_COMMENT,
    UNSET_NAME,
    UNSET_TYPE_NAME,
)
from .enums import EnumsGenerator
from .fragments import FragmentsGenerator
from .init_file import InitFileGenerator
from .input_types import InputTypesGenerator
from .result_types import ResultTypesGenerator
from .scalars import ScalarData, ScalarsDefinitionsGenerator


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
        fragments_module_name: str = "fragments",
        include_comments: bool = True,
        queries_source: str = "",
        schema_source: str = "",
        convert_to_snake_case: bool = True,
        async_client: bool = True,
        fragments: Optional[List[FragmentDefinitionNode]] = None,
        init_generator: Optional[InitFileGenerator] = None,
        client_generator: Optional[ClientGenerator] = None,
        enums_generator: Optional[EnumsGenerator] = None,
        input_types_generator: Optional[InputTypesGenerator] = None,
        files_to_include: Optional[List[str]] = None,
        custom_scalars: Optional[Dict[str, ScalarData]] = None,
        plugin_manager: Optional[PluginManager] = None,
    ) -> None:
        self.package_name = package_name
        self.target_path = target_path
        self.schema = schema
        self.package_path = Path(target_path) / package_name
        self.client_name = client_name
        self.base_client_name = base_client_name
        self.custom_scalars = custom_scalars if custom_scalars else {}

        self.plugin_manager = plugin_manager

        self.base_model_file_path = (
            Path(__file__).parent / "dependencies" / "base_model.py"
        )
        self.base_model_import = generate_import_from(
            [BASE_MODEL_CLASS_NAME], self.base_model_file_path.stem, 1
        )
        self.unset_import = generate_import_from(
            [UNSET_NAME, UNSET_TYPE_NAME], self.base_model_file_path.stem, 1
        )
        self.exceptions_file_path = (
            Path(__file__).parent / "dependencies" / "exceptions.py"
        )

        self.files_to_include = (
            [Path(f) for f in files_to_include] if files_to_include else []
        )

        self.enums_module_name = enums_module_name
        self.input_types_module_name = input_types_module_name
        self.fragments_module_name = fragments_module_name
        self.client_file_name = client_file_name

        self.include_comments = include_comments
        self.queries_source = queries_source
        self.schema_source = schema_source
        self.convert_to_snake_case = convert_to_snake_case
        self.async_client = async_client

        if base_client_file_path:
            self.base_client_file_path = Path(base_client_file_path)
        else:
            if self.async_client:
                self.base_client_file_path = DEFAULT_ASYNC_BASE_CLIENT_PATH
            else:
                self.base_client_file_path = DEFAULT_BASE_CLIENT_PATH

        self.init_generator = (
            init_generator
            if init_generator
            else InitFileGenerator(plugin_manager=self.plugin_manager)
        )
        self.client_generator = (
            client_generator
            if client_generator
            else ClientGenerator(
                name=self.client_name,
                base_client=self.base_client_name,
                enums_module_name=self.enums_module_name,
                input_types_module_name=self.input_types_module_name,
                arguments_generator=ArgumentsGenerator(
                    schema=self.schema,
                    convert_to_snake_case=self.convert_to_snake_case,
                    custom_scalars=self.custom_scalars,
                    plugin_manager=self.plugin_manager,
                ),
                base_client_import=generate_import_from(
                    names=[self.base_client_name],
                    from_=self.base_client_file_path.stem,
                    level=1,
                ),
                unset_import=self.unset_import,
                custom_scalars=self.custom_scalars,
                plugin_manager=self.plugin_manager,
            )
        )
        self.input_types_generator = (
            input_types_generator
            if input_types_generator
            else InputTypesGenerator(
                schema=self.schema,
                enums_module=self.enums_module_name,
                convert_to_snake_case=self.convert_to_snake_case,
                base_model_import=self.base_model_import,
                custom_scalars=self.custom_scalars,
                plugin_manager=self.plugin_manager,
            )
        )
        self.enums_generator = (
            enums_generator
            if enums_generator
            else EnumsGenerator(schema=self.schema, plugin_manager=self.plugin_manager)
        )

        self.fragments_definitions = {f.name.value: f for f in fragments or []}

        self.result_types_files: Dict[str, ast.Module] = {}
        self.generated_files: List[str] = []
        self.include_exceptions_file = self._include_exceptions()

        self.scalars_definitions_generator = ScalarsDefinitionsGenerator(
            scalars_data=list(self.custom_scalars.values()),
            plugin_manager=self.plugin_manager,
        )
        self.scalars_definitions_file_name = "scalars"

        self._unpacked_fragments: Set[str] = set()

    def generate(self) -> List[str]:
        """Generate package with graphql client."""
        self._validate_unique_file_names()
        if not self.package_path.exists():
            self.package_path.mkdir()
        self._generate_enums()
        self._generate_input_types()
        self._generate_result_types()
        self._generate_fragments()
        self._copy_files()
        self._generate_scalars_definitions()
        self._generate_client()
        self._generate_init()

        return sorted(self.generated_files)

    def add_operation(self, definition: OperationDefinitionNode):
        name = definition.name
        if not name:
            raise ParsingError("Query without name.")

        return_type_name = str_to_pascal_case(name.value)
        method_name = process_name(
            name.value,
            convert_to_snake_case=True,
            plugin_manager=self.plugin_manager,
            node=definition,
        )
        module_name = method_name
        file_name = f"{module_name}.py"

        query_types_generator = ResultTypesGenerator(
            schema=self.schema,
            operation_definition=definition,
            enums_module_name=self.enums_module_name,
            fragments_module_name=self.fragments_module_name,
            fragments_definitions=self.fragments_definitions,
            base_model_import=self.base_model_import,
            convert_to_snake_case=self.convert_to_snake_case,
            custom_scalars=self.custom_scalars,
            plugin_manager=self.plugin_manager,
        )
        self._unpacked_fragments = self._unpacked_fragments.union(
            query_types_generator.get_unpacked_fragments()
        )
        self.result_types_files[file_name] = query_types_generator.generate()
        operation_str = query_types_generator.get_operation_as_str()
        self.init_generator.add_import(
            query_types_generator.get_generated_public_names(), module_name, 1
        )

        self.client_generator.add_method(
            definition=definition,
            name=method_name,
            return_type=return_type_name,
            return_type_module=module_name,
            operation_str=operation_str,
            async_=self.async_client,
        )

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
                f"{self.scalars_definitions_file_name}.py",
                f"{self.fragments_module_name}.py",
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
        client_module = self.client_generator.generate()
        code = self._proccess_generated_code(
            ast_to_str(client_module, multiline_strings=True), self.queries_source
        )
        if self.plugin_manager:
            code = self.plugin_manager.generate_client_code(code)
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
        if self.plugin_manager:
            code = self.plugin_manager.generate_enums_code(code)
        enums_file_path = self.package_path / f"{self.enums_module_name}.py"
        enums_file_path.write_text(code)
        self.generated_files.append(enums_file_path.name)
        self.init_generator.add_import(
            self.enums_generator.get_generated_public_names(), self.enums_module_name, 1
        )

    def _generate_input_types(self):
        module = self.input_types_generator.generate()
        input_types_file_path = self.package_path / f"{self.input_types_module_name}.py"
        code = self._proccess_generated_code(ast_to_str(module), self.schema_source)
        if self.plugin_manager:
            code = self.plugin_manager.generate_inputs_code(code)
        input_types_file_path.write_text(code)
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
            if self.plugin_manager:
                code = self.plugin_manager.generate_result_types_code(code)
            file_path.write_text(code)
            self.generated_files.append(file_path.name)

    def _generate_fragments(self):
        if not set(self.fragments_definitions.keys()).difference(
            self._unpacked_fragments
        ):
            return

        generator = FragmentsGenerator(
            schema=self.schema,
            enums_module_name=self.enums_module_name,
            fragments_definitions=self.fragments_definitions,
            exclude_names=self._unpacked_fragments,
            base_model_import=self.base_model_import,
            convert_to_snake_case=self.convert_to_snake_case,
            custom_scalars=self.custom_scalars,
            plugin_manager=self.plugin_manager,
        )
        module = generator.generate()
        file_path = self.package_path / f"{self.fragments_module_name}.py"
        code = self._proccess_generated_code(ast_to_str(module), self.queries_source)
        file_path.write_text(code)
        self.generated_files.append(file_path.name)
        self.init_generator.add_import(
            generator.get_generated_public_names(), self.fragments_module_name, 1
        )

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
            if self.plugin_manager:
                code = self.plugin_manager.copy_code(code)
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

    def _generate_scalars_definitions(self):
        module = self.scalars_definitions_generator.generate()
        scalars_file_path = (
            self.package_path / f"{self.scalars_definitions_file_name}.py"
        )
        code = self._proccess_generated_code(ast_to_str(module))
        if self.plugin_manager:
            code = self.plugin_manager.generate_scalars_code(code)
        scalars_file_path.write_text(code)
        self.generated_files.append(scalars_file_path.name)

    def _generate_init(self):
        init_file_path = self.package_path / "__init__.py"
        init_module = self.init_generator.generate()
        code = self._proccess_generated_code(ast_to_str(init_module, False))
        if self.plugin_manager:
            code = self.plugin_manager.generate_init_code(code)
        init_file_path.write_text(code)
        self.generated_files.append(init_file_path.name)
