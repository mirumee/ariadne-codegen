import ast
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from graphql import (
    ExecutableDefinitionNode,
    FieldNode,
    FragmentDefinitionNode,
    GraphQLEnumType,
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLSchema,
    Node,
    OperationDefinitionNode,
    SelectionSetNode,
    VariableDefinitionNode,
)

from .base import Plugin


# pylint: disable=too-many-public-methods
class PluginManager:
    def __init__(
        self,
        schema: GraphQLSchema,
        config_dict: Optional[Dict] = None,
        plugins_types: Optional[List[Type[Plugin]]] = None,
    ) -> None:
        self.plugins: List[Plugin] = [
            cls(schema=schema, config_dict=config_dict or {})
            for cls in plugins_types or []
        ]

    def _apply_plugins_on_object(
        self, method_name: str, obj: Any, *args, **kwargs
    ) -> Any:
        modified_obj = obj
        for plugin in self.plugins:
            method = getattr(plugin, method_name)
            modified_obj = method(modified_obj, *args, **kwargs)
        return modified_obj

    def generate_init_module(self, module: ast.Module) -> ast.Module:
        return self._apply_plugins_on_object("generate_init_module", module)

    def generate_init_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
        return self._apply_plugins_on_object("generate_init_import", import_)

    def generate_enum(
        self, class_def: ast.ClassDef, enum_type: GraphQLEnumType
    ) -> ast.ClassDef:
        return self._apply_plugins_on_object(
            "generate_enum", class_def, enum_type=enum_type
        )

    def generate_enums_module(self, module: ast.Module) -> ast.Module:
        return self._apply_plugins_on_object("generate_enums_module", module)

    def generate_client_module(self, module: ast.Module) -> ast.Module:
        return self._apply_plugins_on_object("generate_client_module", module)

    def generate_gql_function(self, function_def: ast.FunctionDef) -> ast.FunctionDef:
        return self._apply_plugins_on_object("generate_gql_function", function_def)

    def generate_client_class(self, class_def: ast.ClassDef) -> ast.ClassDef:
        return self._apply_plugins_on_object("generate_client_class", class_def)

    def generate_client_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
        return self._apply_plugins_on_object("generate_client_import", import_)

    def generate_client_method(
        self,
        method_def: Union[ast.FunctionDef, ast.AsyncFunctionDef],
        operation_definition: OperationDefinitionNode,
    ) -> Union[ast.FunctionDef, ast.AsyncFunctionDef]:
        return self._apply_plugins_on_object(
            "generate_client_method",
            method_def,
            operation_definition=operation_definition,
        )

    def generate_arguments(
        self,
        arguments: ast.arguments,
        variable_definitions: Tuple[VariableDefinitionNode, ...],
    ) -> ast.arguments:
        return self._apply_plugins_on_object(
            "generate_arguments", arguments, variable_definitions=variable_definitions
        )

    def generate_arguments_dict(
        self,
        dict_: ast.Dict,
        variable_definitions: Tuple[VariableDefinitionNode, ...],
    ) -> ast.Dict:
        return self._apply_plugins_on_object(
            "generate_arguments_dict", dict_, variable_definitions=variable_definitions
        )

    def generate_inputs_module(self, module: ast.Module) -> ast.Module:
        return self._apply_plugins_on_object("generate_inputs_module", module)

    def generate_input_class(
        self, class_def: ast.ClassDef, input_type: GraphQLInputObjectType
    ) -> ast.ClassDef:
        return self._apply_plugins_on_object(
            "generate_input_class", class_def, input_type=input_type
        )

    def generate_input_field(
        self,
        field_implementation: ast.AnnAssign,
        input_field: GraphQLInputField,
        field_name: str,
    ) -> ast.AnnAssign:
        return self._apply_plugins_on_object(
            "generate_input_field",
            field_implementation,
            input_field=input_field,
            field_name=field_name,
        )

    def generate_result_types_module(
        self, module: ast.Module, operation_definition: ExecutableDefinitionNode
    ) -> ast.Module:
        return self._apply_plugins_on_object(
            "generate_result_types_module",
            module,
            operation_definition=operation_definition,
        )

    def generate_operation_str(
        self, operation_str: str, operation_definition: ExecutableDefinitionNode
    ) -> str:
        return self._apply_plugins_on_object(
            "generate_operation_str",
            operation_str,
            operation_definition=operation_definition,
        )

    def generate_result_class(
        self,
        class_def: ast.ClassDef,
        operation_definition: ExecutableDefinitionNode,
        selection_set: SelectionSetNode,
    ) -> ast.ClassDef:
        return self._apply_plugins_on_object(
            "generate_result_class",
            class_def,
            operation_definition=operation_definition,
            selection_set=selection_set,
        )

    def generate_result_field(
        self,
        field_implementation: ast.AnnAssign,
        operation_definition: ExecutableDefinitionNode,
        field: FieldNode,
    ) -> ast.AnnAssign:
        return self._apply_plugins_on_object(
            "generate_result_field",
            field_implementation,
            operation_definition=operation_definition,
            field=field,
        )

    def generate_client_code(self, generated_code: str) -> str:
        return self._apply_plugins_on_object("generate_client_code", generated_code)

    def generate_enums_code(self, generated_code: str) -> str:
        return self._apply_plugins_on_object("generate_enums_code", generated_code)

    def generate_inputs_code(self, generated_code: str) -> str:
        return self._apply_plugins_on_object("generate_inputs_code", generated_code)

    def generate_result_types_code(self, generated_code: str) -> str:
        return self._apply_plugins_on_object(
            "generate_result_types_code", generated_code
        )

    def copy_code(self, copied_code: str) -> str:
        return self._apply_plugins_on_object("copy_code", copied_code)

    def generate_init_code(self, generated_code: str) -> str:
        return self._apply_plugins_on_object("generate_init_code", generated_code)

    def process_name(self, name: str, node: Optional[Node] = None) -> str:
        return self._apply_plugins_on_object("process_name", name, node=node)

    def generate_fragments_module(
        self,
        module: ast.Module,
        fragments_definitions: Dict[str, FragmentDefinitionNode],
    ) -> ast.Module:
        return self._apply_plugins_on_object(
            "generate_fragments_module",
            module,
            fragments_definitions=fragments_definitions,
        )

    def process_schema(self, schema: GraphQLSchema) -> GraphQLSchema:
        processed_schema = schema
        for plugin in self.plugins:
            processed_schema = plugin.process_schema(processed_schema)

            for plugin in self.plugins:
                plugin.schema = processed_schema

        return processed_schema

    def get_file_comment(
        self, comment: str, code: str, source: Optional[str] = None
    ) -> str:
        return self._apply_plugins_on_object(
            "get_file_comment", comment, code=code, source=source
        )
