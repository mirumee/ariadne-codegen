import ast
from typing import Dict, Tuple, Union

from graphql import (
    FieldNode,
    GraphQLEnumType,
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLSchema,
    OperationDefinitionNode,
    SelectionSetNode,
    VariableDefinitionNode,
)


# pylint: disable=too-many-public-methods
class Plugin:
    def __init__(self, schema: GraphQLSchema, config_dict: Dict) -> None:
        self.schema = schema
        self.config_dict = config_dict

    def generate_init_module(self, module: ast.Module) -> ast.Module:
        return module

    def generate_init_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
        return import_

    # pylint: disable=unused-argument
    def generate_enum(
        self, class_def: ast.ClassDef, enum_type: GraphQLEnumType
    ) -> ast.ClassDef:
        return class_def

    def generate_enums_module(self, module: ast.Module) -> ast.Module:
        return module

    def generate_client_module(self, module: ast.Module) -> ast.Module:
        return module

    def generate_gql_function(self, function_def: ast.FunctionDef) -> ast.FunctionDef:
        return function_def

    def generate_client_class(self, class_def: ast.ClassDef) -> ast.ClassDef:
        return class_def

    def generate_client_import(self, import_: ast.ImportFrom) -> ast.ImportFrom:
        return import_

    def generate_client_method(
        self, method_def: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> Union[ast.FunctionDef, ast.AsyncFunctionDef]:
        return method_def

    # pylint: disable=unused-argument
    def generate_arguments(
        self,
        arguments: ast.arguments,
        variable_definitions: Tuple[VariableDefinitionNode, ...],
    ) -> ast.arguments:
        return arguments

    # pylint: disable=unused-argument
    def generate_arguments_dict(
        self,
        dict_: ast.Dict,
        variable_definitions: Tuple[VariableDefinitionNode, ...],
    ) -> ast.Dict:
        return dict_

    def generate_inputs_module(self, module: ast.Module) -> ast.Module:
        return module

    # pylint: disable=unused-argument
    def generate_input_class(
        self, class_def: ast.ClassDef, input_type: GraphQLInputObjectType
    ) -> ast.ClassDef:
        return class_def

    # pylint: disable=unused-argument
    def generate_input_field(
        self,
        field_implementation: ast.AnnAssign,
        input_field: GraphQLInputField,
        field_name: str,
    ) -> ast.AnnAssign:
        return field_implementation

    # pylint: disable=unused-argument
    def generate_result_types_module(
        self, module: ast.Module, operation_definition: OperationDefinitionNode
    ) -> ast.Module:
        return module

    # pylint: disable=unused-argument
    def generate_operation_str(
        self, operation_str: str, operation_definition: OperationDefinitionNode
    ) -> str:
        return operation_str

    # pylint: disable=unused-argument
    def generate_result_class(
        self,
        class_def: ast.ClassDef,
        operation_definition: OperationDefinitionNode,
        selection_set: SelectionSetNode,
    ) -> ast.ClassDef:
        return class_def

    # pylint: disable=unused-argument
    def generate_result_field(
        self,
        field_implementation: ast.AnnAssign,
        operation_definition: OperationDefinitionNode,
        field: FieldNode,
    ) -> ast.AnnAssign:
        return field_implementation

    def generate_scalars_module(self, module: ast.Module) -> ast.Module:
        return module

    def generate_scalars_parse_dict(self, dict_: ast.Dict) -> ast.Dict:
        return dict_

    def generate_scalars_serialize_dict(self, dict_: ast.Dict) -> ast.Dict:
        return dict_
