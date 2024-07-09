from typing import Any, Dict, List, Tuple

from graphql import (
    DocumentNode,
    NamedTypeNode,
    NameNode,
    OperationDefinitionNode,
    OperationType,
    SelectionSetNode,
    VariableDefinitionNode,
    VariableNode,
    print_ast,
)

from .async_base_client import AsyncBaseClient
from .base_operation import GraphQLField


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def execute_custom_operation(
        self, *fields: GraphQLField, operation_type: OperationType, operation_name: str
    ) -> Dict[str, Any]:
        variables_types_combined, processed_variables_combined = (
            self._combine_variables(fields)
        )
        variable_definitions = self._build_variable_definitions(
            variables_types_combined
        )
        operation_ast = self._build_operation_ast(
            fields, operation_type, operation_name, variable_definitions
        )
        response = await self.execute(
            print_ast(operation_ast),
            variables=processed_variables_combined,
            operation_name=operation_name,
        )
        return self.get_data(response)

    def _combine_variables(
        self, fields: Tuple[GraphQLField, ...]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        variables_types_combined = {}
        processed_variables_combined = {}
        for idx, field in enumerate(fields):
            variables_types_combined.update(field.get_variables_types(idx))
            processed_variables_combined.update(field.get_processed_variables(idx))
        return (variables_types_combined, processed_variables_combined)

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
        fields: Tuple[GraphQLField, ...],
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
                    selection_set=SelectionSetNode(
                        selections=[
                            field.to_ast(idx) for idx, field in enumerate(fields)
                        ]
                    ),
                )
            ]
        )

    async def query(self, *fields: GraphQLField, operation_name: str) -> Dict[str, Any]:
        return await self.execute_custom_operation(
            *fields, operation_type=OperationType.QUERY, operation_name=operation_name
        )

    async def mutation(
        self, *fields: GraphQLField, operation_name: str
    ) -> Dict[str, Any]:
        return await self.execute_custom_operation(
            *fields,
            operation_type=OperationType.MUTATION,
            operation_name=operation_name
        )
