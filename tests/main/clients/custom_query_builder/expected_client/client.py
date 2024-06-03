from typing import Any, Dict

import httpx

from .async_base_client import AsyncBaseClient
from .base_operation import BaseGraphQLOperation
from .list_all_products import ListAllProducts
from .operations import LIST_ALL_PRODUCTS_GQL


def gql(q: str) -> str:
    return q


class AutoGenClient(AsyncBaseClient):
    async def list_all_products(self, **kwargs: Any) -> ListAllProducts:
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=LIST_ALL_PRODUCTS_GQL,
            operation_name="ListAllProducts",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return ListAllProducts.model_validate(data)

    async def query(
        self, *queries: BaseGraphQLOperation, operation_name: str
    ) -> httpx.Response:
        query_str = f"""
            query {operation_name} {{ {" ".join([str(query) for query in queries])} }}
            """
        return await self.execute(query_str, operation_name=operation_name)
