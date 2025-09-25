import ast
from typing import Dict, List, Optional, cast

from graphql import (
    GraphQLFieldMap,
    GraphQLInterfaceType,
    GraphQLObjectType,
    GraphQLUnionType,
)

from ariadne_codegen.client_generators.custom_arguments import ArgumentGenerator

from ..codegen import (
    generate_call,
    generate_class_def,
    generate_constant,
    generate_import_from,
    generate_keyword,
    generate_method_definition,
    generate_module,
    generate_name,
    generate_return,
)
from ..plugins.manager import PluginManager
from ..utils import str_to_snake_case
from .arguments import ArgumentsGenerator
from .constants import (
    ANY,
    CUSTOM_FIELDS_FILE_PATH,
    CUSTOM_FIELDS_TYPING_FILE_PATH,
    DICT,
    GRAPHQL_BASE_FIELD_CLASS,
    GRAPHQL_INTERFACE_SUFFIX,
    GRAPHQL_OBJECT_SUFFIX,
    GRAPHQL_UNION_SUFFIX,
    OPTIONAL,
    TYPING_MODULE,
)
from .custom_generator_utils import get_final_type
from .scalars import ScalarData


class CustomOperationGenerator:
    """
    Generates custom operations for a given GraphQL schema using Python's AST module.
    """

    def __init__(
        self,
        graphql_fields: GraphQLFieldMap,
        name: str,
        base_name: str,
        arguments_generator: ArgumentsGenerator,
        enums_module_name: str = "enums",
        custom_scalars: Optional[Dict[str, ScalarData]] = None,
        plugin_manager: Optional[PluginManager] = None,
        convert_to_snake_case: bool = True,
    ) -> None:
        self.graphql_fields = graphql_fields
        self.name = name
        self.base_name = base_name
        self.enums_module_name = enums_module_name
        self.plugin_manager = plugin_manager
        self.custom_scalars = custom_scalars if custom_scalars else {}
        self.arguments_generator = arguments_generator
        self.convert_to_snake_case = convert_to_snake_case

        self._imports: List[ast.ImportFrom] = []
        self._type_imports: List[ast.ImportFrom] = []
        self._add_import(generate_import_from([OPTIONAL, ANY, DICT], TYPING_MODULE))
        self.argument_generator = ArgumentGenerator(
            self.custom_scalars,
            self.convert_to_snake_case,
            self.plugin_manager,
        )

        self._class_def = generate_class_def(name=name, base_names=[])

    def generate(self) -> ast.Module:
        """Generate module with class definition of graphql client."""
        for name, field in self.graphql_fields.items():
            final_type = get_final_type(field)
            method_def = self._generate_method(
                operation_name=name,
                operation_args=field.args,
                final_type=final_type,
                description=field.description,
            )
            method_def.lineno = len(self._class_def.body) + 1
            self._class_def.body.append(method_def)

        if not self._class_def.body:
            self._class_def.body.append(ast.Pass())

        self.argument_generator.add_custom_scalar_imports()

        self._class_def.lineno = len(self._imports) + 3

        module = generate_module(
            body=cast(List[ast.stmt], self._imports)
            + cast(List[ast.stmt], self._type_imports)
            + [self._class_def],
        )
        return module

    def _add_import(self, import_: Optional[ast.ImportFrom] = None):
        """Adds an import statement to the list of imports."""
        if import_:
            if self.plugin_manager:
                import_ = self.plugin_manager.generate_client_import(import_)
            if import_.names and import_.module:
                self._imports.append(import_)

    def _generate_method(
        self,
        operation_name: str,
        operation_args,
        final_type,
        description: Optional[str] = None,
    ) -> ast.FunctionDef:
        """Generates a method definition for a given operation."""
        (
            method_arguments,
            return_arguments_keys,
            return_arguments_values,
        ) = self.argument_generator.generate_arguments(operation_args)
        self._imports.extend(self.argument_generator.imports)

        return_type_name = self._get_return_type_and_from(final_type)

        arguments_body: List[ast.stmt] = []
        arguments_keyword: List[ast.keyword] = []

        if operation_args:
            (
                arguments_body,
                arguments_keyword,
            ) = self.argument_generator.generate_clear_arguments_section(
                return_arguments_keys, return_arguments_values
            )

        return generate_method_definition(
            name=str_to_snake_case(operation_name),
            arguments=method_arguments,
            return_type=generate_name(return_type_name),
            description=description,
            body=[
                *arguments_body,
                generate_return(
                    value=generate_call(
                        func=generate_name(return_type_name),
                        args=[],
                        keywords=[
                            generate_keyword(
                                arg="field_name",
                                value=generate_constant(value=operation_name),
                            ),
                            *arguments_keyword,
                        ],
                    )
                ),
            ],
            decorator_list=[generate_name("classmethod")],
        )

    def _get_return_type_and_from(self, final_type):
        """
        Determines the return type name and its import path based on the final type.
        """
        if isinstance(final_type, GraphQLObjectType):
            return_type_name = f"{final_type.name}{GRAPHQL_OBJECT_SUFFIX}"
            from_ = CUSTOM_FIELDS_FILE_PATH.stem
        elif isinstance(final_type, GraphQLInterfaceType):
            return_type_name = f"{final_type.name}{GRAPHQL_INTERFACE_SUFFIX}"
            from_ = CUSTOM_FIELDS_FILE_PATH.stem
        elif isinstance(final_type, GraphQLUnionType):
            return_type_name = f"{final_type.name}{GRAPHQL_UNION_SUFFIX}"
            from_ = CUSTOM_FIELDS_TYPING_FILE_PATH.stem
        else:
            return_type_name = GRAPHQL_BASE_FIELD_CLASS
            from_ = CUSTOM_FIELDS_TYPING_FILE_PATH.stem
        self._type_imports.append(
            generate_import_from(
                from_=from_,
                names=[return_type_name],
                level=1,
            )
        )
        return return_type_name

    @staticmethod
    def _capitalize_first_letter(s: str) -> str:
        """Capitalizes the first letter of the given string."""
        return s[0].upper() + s[1:]
