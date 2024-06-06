import ast
from pathlib import Path
from typing import Dict, List, Optional, Set

from graphql import (
    FragmentDefinitionNode,
    GraphQLSchema,
    OperationDefinitionNode,
    OperationType,
)

from ..codegen import generate_import_from
from ..exceptions import ParsingError
from ..plugins.manager import PluginManager
from ..settings import ClientSettings, CommentsStrategy
from ..utils import ast_to_str, process_name, str_to_pascal_case
from .arguments import ArgumentsGenerator
from .client import ClientGenerator
from .comments import get_comment
from .constants import (
    BASE_GRAPHQL_OPERATION_CLASS_NAME,
    BASE_MODEL_CLASS_NAME,
    BASE_MODEL_FILE_PATH,
    BASE_MODEL_IMPORT,
    BASE_OPERATION_FILE_PATH,
    DEFAULT_ASYNC_BASE_CLIENT_OPEN_TELEMETRY_PATH,
    DEFAULT_ASYNC_BASE_CLIENT_PATH,
    DEFAULT_BASE_CLIENT_OPEN_TELEMETRY_PATH,
    DEFAULT_BASE_CLIENT_PATH,
    EXCEPTIONS_FILE_PATH,
    GRAPHQL_CLIENT_EXCEPTIONS_NAMES,
    UNSET_IMPORT,
    UPLOAD_CLASS_NAME,
    UPLOAD_IMPORT,
)
from .custom_fields import CustomFieldsGenerator
from .custom_fields_typing import CustomFieldsTypingGenerator
from .custom_operation import CustomOperationGenerator
from .enums import EnumsGenerator
from .fragments import FragmentsGenerator
from .init_file import InitFileGenerator
from .input_types import InputTypesGenerator
from .result_types import ResultTypesGenerator
from .scalars import ScalarData


class PackageGenerator:
    def __init__(
        self,
        package_name: str,
        target_path: str,
        schema: GraphQLSchema,
        init_generator: InitFileGenerator,
        client_generator: ClientGenerator,
        enums_generator: EnumsGenerator,
        input_types_generator: InputTypesGenerator,
        fragments_generator: FragmentsGenerator,
        custom_fields_generator: Optional[CustomFieldsGenerator] = None,
        custom_fields_typing_generator: Optional[CustomFieldsTypingGenerator] = None,
        custom_query_generator: Optional[CustomOperationGenerator] = None,
        custom_mutation_generator: Optional[CustomOperationGenerator] = None,
        fragments_definitions: Optional[Dict[str, FragmentDefinitionNode]] = None,
        client_name: str = "Client",
        async_client: bool = True,
        base_client_name: str = "AsyncBaseClient",
        base_client_file_path: str = DEFAULT_ASYNC_BASE_CLIENT_PATH.as_posix(),
        client_file_name: str = "client",
        enums_module_name: str = "enums",
        input_types_module_name: str = "input_types",
        fragments_module_name: str = "fragments",
        custom_help_field_module_name: str = "custom_typing_fields",
        comments_strategy: CommentsStrategy = CommentsStrategy.STABLE,
        queries_source: str = "",
        schema_source: str = "",
        convert_to_snake_case: bool = True,
        include_all_inputs: bool = True,
        include_all_enums: bool = True,
        base_model_file_path: str = BASE_MODEL_FILE_PATH.as_posix(),
        base_schema_root_file_path: str = BASE_OPERATION_FILE_PATH.as_posix(),
        base_model_import: ast.ImportFrom = BASE_MODEL_IMPORT,
        upload_import: ast.ImportFrom = UPLOAD_IMPORT,
        unset_import: ast.ImportFrom = UNSET_IMPORT,
        files_to_include: Optional[List[str]] = None,
        custom_scalars: Optional[Dict[str, ScalarData]] = None,
        plugin_manager: Optional[PluginManager] = None,
        enable_custom_operations: bool = False,
    ) -> None:
        self.package_path = Path(target_path) / package_name

        self.schema = schema
        self.fragments_definitions = (
            fragments_definitions if fragments_definitions else {}
        )

        self.init_generator = init_generator
        self.client_generator = client_generator
        self.enums_generator = enums_generator
        self.input_types_generator = input_types_generator
        self.fragments_generator = fragments_generator
        self.custom_fields_generator = custom_fields_generator
        self.custom_query_generator = custom_query_generator
        self.custom_mutation_generator = custom_mutation_generator
        self.custom_fields_typing_generator = custom_fields_typing_generator
        self.custom_help_field_module_name = custom_help_field_module_name

        self.client_name = client_name
        self.async_client = async_client
        self.base_client_name = base_client_name
        self.base_client_file_path = Path(base_client_file_path)

        self.client_file_name = client_file_name
        self.enums_module_name = enums_module_name
        self.input_types_module_name = input_types_module_name
        self.fragments_module_name = fragments_module_name

        self.comments_strategy = comments_strategy
        self.queries_source = queries_source
        self.schema_source = schema_source

        self.convert_to_snake_case = convert_to_snake_case
        self.include_all_inputs = include_all_inputs
        self.include_all_enums = include_all_enums

        self.base_model_file_path = Path(base_model_file_path)
        self.base_model_import = base_model_import
        self.upload_import = upload_import
        self.unset_import = unset_import

        self.base_schema_root_file_path = Path(base_schema_root_file_path)

        self.files_to_include = (
            [Path(f) for f in files_to_include] if files_to_include else []
        )
        self.custom_scalars = custom_scalars if custom_scalars else {}
        self.plugin_manager = plugin_manager

        self._result_types_files: Dict[str, ast.Module] = {}
        self._generated_files: List[str] = []
        self._unpacked_fragments: Set[str] = set()
        self._used_enums: List[str] = []

        self.enable_custom_operations = enable_custom_operations
        if self.enable_custom_operations:
            self.files_to_include.append(self.base_schema_root_file_path)

    def generate(self) -> List[str]:
        """Generate package with graphql client."""
        self._include_exceptions()
        self._validate_unique_file_names()
        if not self.package_path.exists():
            self.package_path.mkdir()
        self._generate_input_types()
        self._generate_result_types()
        self._generate_fragments()
        self._copy_files()
        if self.enable_custom_operations:
            self._generate_custom_fields_typing()
            self._generate_custom_fields()
            self.client_generator.add_execute_custom_operation_method()
            if self.custom_query_generator:
                self._generate_custom_queries()
                self.client_generator.create_custom_operation_method(
                    "query", OperationType.QUERY.value.upper()
                )
            if self.custom_mutation_generator:
                self._generate_custom_mutations()
                self.client_generator.create_custom_operation_method(
                    "mutation", OperationType.MUTATION.value.upper()
                )

        self._generate_client()
        self._generate_enums()
        self._generate_init()

        return sorted(self._generated_files)

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
        self._used_enums.extend(query_types_generator.get_used_enums())
        self._result_types_files[file_name] = query_types_generator.generate()
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
        if self.base_client_file_path in (
            DEFAULT_ASYNC_BASE_CLIENT_PATH,
            DEFAULT_BASE_CLIENT_PATH,
            DEFAULT_ASYNC_BASE_CLIENT_OPEN_TELEMETRY_PATH,
            DEFAULT_BASE_CLIENT_OPEN_TELEMETRY_PATH,
        ):
            self.files_to_include.append(EXCEPTIONS_FILE_PATH)
            self.init_generator.add_import(
                names=GRAPHQL_CLIENT_EXCEPTIONS_NAMES,
                from_=EXCEPTIONS_FILE_PATH.stem,
                level=1,
            )

    def _validate_unique_file_names(self):
        file_names = (
            [
                f"{self.client_file_name}.py",
                self.base_client_file_path.name,
                self.base_model_file_path.name,
                f"{self.enums_module_name}.py",
                f"{self.input_types_module_name}.py",
                f"{self.fragments_module_name}.py",
            ]
            + list(self._result_types_files.keys())
            + [f.name for f in self.files_to_include]
        )

        if len(file_names) != len(set(file_names)):
            seen = set()
            duplicated_files = {n for n in file_names if n in seen or seen.add(n)}
            raise ParsingError(f"Duplicated file names: {',' .join(duplicated_files)}")

    def _generate_client(self):
        client_file_path = self.package_path / f"{self.client_file_name}.py"
        client_module = self.client_generator.generate()
        code = self._add_comments_to_code(
            ast_to_str(client_module, multiline_strings=True), self.queries_source
        )
        if self.plugin_manager:
            code = self.plugin_manager.generate_client_code(code)
        client_file_path.write_text(code)
        self._generated_files.append(client_file_path.name)
        self._used_enums.extend(
            self.client_generator.arguments_generator.get_used_enums()
        )
        self.init_generator.add_import(
            names=[self.client_generator.name], from_=self.client_file_name, level=1
        )

    def _add_comments_to_code(self, code: str, source: Optional[str] = None) -> str:
        comment = get_comment(strategy=self.comments_strategy, source=source)
        if self.plugin_manager:
            comment = self.plugin_manager.get_file_comment(
                comment, code=code, source=source
            )
        if comment:
            return comment + "\n\n" + code

        return code

    def _generate_enums(self):
        if self.include_all_enums:
            module = self.enums_generator.generate()
        else:
            module = self.enums_generator.generate(types_to_include=self._used_enums)

        code = self._add_comments_to_code(ast_to_str(module), self.schema_source)
        if self.plugin_manager:
            code = self.plugin_manager.generate_enums_code(code)
        enums_file_path = self.package_path / f"{self.enums_module_name}.py"
        enums_file_path.write_text(code)
        self._generated_files.append(enums_file_path.name)
        self.init_generator.add_import(
            self.enums_generator.get_generated_public_names(), self.enums_module_name, 1
        )

    def _generate_input_types(self):
        if self.include_all_inputs:
            module = self.input_types_generator.generate()
        else:
            used_inputs = self.client_generator.arguments_generator.get_used_inputs()
            module = self.input_types_generator.generate(types_to_include=used_inputs)

        input_types_file_path = self.package_path / f"{self.input_types_module_name}.py"
        code = self._add_comments_to_code(ast_to_str(module), self.schema_source)
        if self.plugin_manager:
            code = self.plugin_manager.generate_inputs_code(code)
        input_types_file_path.write_text(code)
        self._generated_files.append(input_types_file_path.name)
        self._used_enums.extend(self.input_types_generator.get_used_enums())
        self.init_generator.add_import(
            self.input_types_generator.get_generated_public_names(),
            self.input_types_module_name,
            1,
        )

    def _generate_result_types(self):
        for file_name, module in self._result_types_files.items():
            file_path = self.package_path / file_name
            code = self._add_comments_to_code(ast_to_str(module), self.queries_source)
            if self.plugin_manager:
                code = self.plugin_manager.generate_result_types_code(code)
            file_path.write_text(code)
            self._generated_files.append(file_path.name)

    def _generate_fragments(self):
        if not set(self.fragments_definitions.keys()).difference(
            self._unpacked_fragments
        ):
            return

        module = self.fragments_generator.generate(
            exclude_names=self._unpacked_fragments
        )
        file_path = self.package_path / f"{self.fragments_module_name}.py"
        code = self._add_comments_to_code(ast_to_str(module), self.queries_source)
        file_path.write_text(code)
        self._generated_files.append(file_path.name)
        self._used_enums.extend(self.fragments_generator.get_used_enums())
        self.init_generator.add_import(
            self.fragments_generator.get_generated_public_names(),
            self.fragments_module_name,
            1,
        )

    def _copy_files(self):
        files_to_copy = self.files_to_include + [
            self.base_client_file_path,
            self.base_model_file_path,
        ]
        for source_path in files_to_copy:
            code = self._add_comments_to_code(source_path.read_text(encoding="utf-8"))
            if self.plugin_manager:
                code = self.plugin_manager.copy_code(code)
            target_path = self.package_path / source_path.name
            target_path.write_text(code)
            self._generated_files.append(target_path.name)

        self.init_generator.add_import(
            names=[self.base_client_name],
            from_=self.base_client_file_path.stem,
            level=1,
        )
        self.init_generator.add_import(
            names=[BASE_MODEL_CLASS_NAME, UPLOAD_CLASS_NAME],
            from_=self.base_model_file_path.stem,
            level=1,
        )

    def _generate_init(self):
        init_file_path = self.package_path / "__init__.py"
        init_module = self.init_generator.generate()
        code = self._add_comments_to_code(ast_to_str(init_module, False))
        if self.plugin_manager:
            code = self.plugin_manager.generate_init_code(code)
        init_file_path.write_text(code)
        self._generated_files.append(init_file_path.name)

    def _generate_custom_queries(self):
        file_path = self.package_path / "custom_queries.py"
        module = self.custom_query_generator.generate()
        code = self._add_comments_to_code(ast_to_str(module, False))
        file_path.write_text(code)
        self._generated_files.append(file_path.name)

    def _generate_custom_mutations(self):
        file_path = self.package_path / "custom_mutations.py"
        module = self.custom_mutation_generator.generate()
        code = self._add_comments_to_code(ast_to_str(module, False))
        file_path.write_text(code)
        self._generated_files.append(file_path.name)

    def _generate_custom_fields_typing(self):
        file_path = self.package_path / "custom_typing_fields.py"
        module = self.custom_fields_typing_generator.generate()
        code = self._add_comments_to_code(ast_to_str(module, False))
        file_path.write_text(code)
        self._generated_files.append(file_path.name)
        self.init_generator.add_import(
            self.custom_fields_typing_generator.get_generated_public_names(),
            self.custom_help_field_module_name,
            1,
        )

    def _generate_custom_fields(self):
        file_path = self.package_path / "custom_fields.py"
        module = self.custom_fields_generator.generate()
        code = self._add_comments_to_code(ast_to_str(module, False))
        file_path.write_text(code)
        self._generated_files.append(file_path.name)


def get_package_generator(
    schema: GraphQLSchema,
    fragments: List[FragmentDefinitionNode],
    settings: ClientSettings,
    plugin_manager: PluginManager,
) -> PackageGenerator:
    init_generator = InitFileGenerator(plugin_manager=plugin_manager)
    client_generator = ClientGenerator(
        base_client_import=generate_import_from(
            names=[settings.base_client_name],
            from_=Path(settings.base_client_file_path).stem,
            level=1,
        ),
        arguments_generator=ArgumentsGenerator(
            schema=schema,
            convert_to_snake_case=settings.convert_to_snake_case,
            custom_scalars=settings.scalars,
            plugin_manager=plugin_manager,
        ),
        name=settings.client_name,
        base_client=settings.base_client_name,
        enums_module_name=settings.enums_module_name,
        input_types_module_name=settings.input_types_module_name,
        unset_import=UNSET_IMPORT,
        upload_import=UPLOAD_IMPORT,
        custom_scalars=settings.scalars,
        plugin_manager=plugin_manager,
    )
    enums_generator = EnumsGenerator(schema=schema, plugin_manager=plugin_manager)
    input_types_generator = InputTypesGenerator(
        schema=schema,
        enums_module=settings.enums_module_name,
        base_model_import=BASE_MODEL_IMPORT,
        upload_import=UPLOAD_IMPORT,
        convert_to_snake_case=settings.convert_to_snake_case,
        custom_scalars=settings.scalars,
        plugin_manager=plugin_manager,
    )
    fragments_definitions = {f.name.value: f for f in fragments or []}
    fragments_generator = FragmentsGenerator(
        schema=schema,
        fragments_definitions=fragments_definitions,
        enums_module_name=settings.enums_module_name,
        base_model_import=BASE_MODEL_IMPORT,
        convert_to_snake_case=settings.convert_to_snake_case,
        custom_scalars=settings.scalars,
        plugin_manager=plugin_manager,
    )
    custom_fields_generator = CustomFieldsGenerator(schema=schema)
    custom_fields_typing_generator = CustomFieldsTypingGenerator(schema=schema)
    custom_query_generator = None
    if schema.query_type:
        custom_query_generator = CustomOperationGenerator(
            graphql_fields=schema.query_type.fields,
            name="Query",
            base_name=BASE_GRAPHQL_OPERATION_CLASS_NAME,
            enums_module_name=settings.enums_module_name,
            custom_scalars=settings.scalars,
            plugin_manager=plugin_manager,
        )
    custom_mutation_generator = None
    if schema.mutation_type:
        custom_mutation_generator = CustomOperationGenerator(
            graphql_fields=schema.mutation_type.fields,
            name="Mutation",
            base_name=BASE_GRAPHQL_OPERATION_CLASS_NAME,
            enums_module_name=settings.enums_module_name,
            custom_scalars=settings.scalars,
            plugin_manager=plugin_manager,
        )

    return PackageGenerator(
        package_name=settings.target_package_name,
        target_path=settings.target_package_path,
        schema=schema,
        init_generator=init_generator,
        client_generator=client_generator,
        enums_generator=enums_generator,
        input_types_generator=input_types_generator,
        fragments_generator=fragments_generator,
        fragments_definitions=fragments_definitions,
        client_name=settings.client_name,
        async_client=settings.async_client,
        base_client_name=settings.base_client_name,
        base_client_file_path=settings.base_client_file_path,
        client_file_name=settings.client_file_name,
        enums_module_name=settings.enums_module_name,
        input_types_module_name=settings.input_types_module_name,
        fragments_module_name=settings.fragments_module_name,
        custom_fields_generator=custom_fields_generator,
        custom_fields_typing_generator=custom_fields_typing_generator,
        custom_query_generator=custom_query_generator,
        custom_mutation_generator=custom_mutation_generator,
        comments_strategy=settings.include_comments,
        queries_source=settings.queries_path,
        schema_source=settings.schema_source,
        convert_to_snake_case=settings.convert_to_snake_case,
        include_all_inputs=settings.include_all_inputs,
        include_all_enums=settings.include_all_enums,
        base_model_file_path=BASE_MODEL_FILE_PATH.as_posix(),
        base_model_import=BASE_MODEL_IMPORT,
        upload_import=UPLOAD_IMPORT,
        unset_import=UNSET_IMPORT,
        files_to_include=settings.files_to_include,
        custom_scalars=settings.scalars,
        plugin_manager=plugin_manager,
        enable_custom_operations=settings.enable_custom_operations,
    )
