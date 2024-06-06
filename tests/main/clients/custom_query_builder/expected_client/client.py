from typing import Any, Dict

from graphql import (
    DocumentNode,
    NameNode,
    OperationDefinitionNode,
    OperationType,
    SelectionSetNode,
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
        operation_ast = DocumentNode(
            definitions=[
                OperationDefinitionNode(
                    operation=operation_type,
                    name=NameNode(value=operation_name),
                    selection_set=SelectionSetNode(
                        selections=[field.to_ast() for field in fields]
                    ),
                )
            ]
        )
        response = await self.execute(
            print_ast(operation_ast), operation_name=operation_name
        )
        return self.get_data(response)

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
