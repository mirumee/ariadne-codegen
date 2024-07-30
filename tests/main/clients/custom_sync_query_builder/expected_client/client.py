from typing import Any, Dict, List, Tuple

from graphql import (
    DocumentNode,
    NamedTypeNode,
    NameNode,
    OperationDefinitionNode,
    OperationType,
    SelectionNode,
    SelectionSetNode,
    VariableDefinitionNode,
    VariableNode,
    print_ast,
)

from .base_client import BaseClient
from .base_operation import GraphQLField


def gql(q: str) -> str:
    return q


class Client(BaseClient):
    def execute_custom_operation(
        self, *fields: GraphQLField, operation_type: OperationType, operation_name: str
    ) -> Dict[str, Any]:
        selections = self._build_selection_set(fields)
        combined_variables = self._combine_variables(fields)
        variable_definitions = self._build_variable_definitions(
            combined_variables["types"]
        )
        operation_ast = self._build_operation_ast(
            selections, operation_type, operation_name, variable_definitions
        )
        response = self.execute(
            print_ast(operation_ast),
            variables=combined_variables["values"],
            operation_name=operation_name,
        )
        return self.get_data(response)

    def _combine_variables(
        self, fields: Tuple[GraphQLField, ...]
    ) -> Dict[str, Dict[str, Any]]:
        variables_types_combined = {}
        processed_variables_combined = {}
        for field in fields:
            formatted_variables = field.get_formatted_variables()
            variables_types_combined.update(
                {k: v["type"] for k, v in formatted_variables.items()}
            )
            processed_variables_combined.update(
                {k: v["value"] for k, v in formatted_variables.items()}
            )
        return {
            "types": variables_types_combined,
            "values": processed_variables_combined,
        }

    def _build_variable_definitions(
        self, variables_types_combined: Dict[str, str]
    ) -> List[VariableDefinitionNode]:
        return [
            VariableDefinitionNode(
                variable=VariableNode(name=NameNode(value=var_name)),
                type=NamedTypeNode(name=NameNode(value=var_value)),
            )
            for var_name, var_value in variables_types_combined.items()
        ]

    def _build_operation_ast(
        self,
        selections: List[SelectionNode],
        operation_type: OperationType,
        operation_name: str,
        variable_definitions: List[VariableDefinitionNode],
    ) -> DocumentNode:
        return DocumentNode(
            definitions=[
                OperationDefinitionNode(
                    operation=operation_type,
                    name=NameNode(value=operation_name),
                    variable_definitions=variable_definitions,
                    selection_set=SelectionSetNode(selections=selections),
                )
            ]
        )

    def _build_selection_set(
        self, fields: Tuple[GraphQLField, ...]
    ) -> List[SelectionNode]:
        return [field.to_ast(idx) for idx, field in enumerate(fields)]

    def query(self, *fields: GraphQLField, operation_name: str) -> Dict[str, Any]:
        return self.execute_custom_operation(
            *fields, operation_type=OperationType.QUERY, operation_name=operation_name
        )

    def mutation(self, *fields: GraphQLField, operation_name: str) -> Dict[str, Any]:
        return self.execute_custom_operation(
            *fields,
            operation_type=OperationType.MUTATION,
            operation_name=operation_name
        )
