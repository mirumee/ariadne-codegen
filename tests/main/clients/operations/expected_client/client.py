from typing import Any, AsyncIterator, Dict

from .async_base_client import AsyncBaseClient
from .c_mutation import CMutation
from .c_query import CQuery
from .c_subscription import CSubscription
from .custom_operations import (
    C_MUTATION_GQL,
    C_QUERY_GQL,
    C_SUBSCRIPTION_GQL,
    GET_A_GQL,
    GET_A_WITH_FRAGMENT_GQL,
    GET_XYZ_GQL,
)
from .get_a import GetA
from .get_a_with_fragment import GetAWithFragment
from .get_xyz import GetXYZ


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def c_query(self, **kwargs: Any) -> CQuery:
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=C_QUERY_GQL, operation_name="cQuery", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return CQuery.model_validate(data)

    async def c_mutation(self, **kwargs: Any) -> CMutation:
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=C_MUTATION_GQL,
            operation_name="cMutation",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return CMutation.model_validate(data)

    async def c_subscription(self, **kwargs: Any) -> AsyncIterator[CSubscription]:
        variables: Dict[str, object] = {}
        async for data in self.execute_ws(
            query=C_SUBSCRIPTION_GQL, variables=variables, **kwargs
        ):
            yield CSubscription.model_validate(data)

    async def get_a(self, **kwargs: Any) -> GetA:
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=GET_A_GQL, operation_name="getA", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetA.model_validate(data)

    async def get_a_with_fragment(self, **kwargs: Any) -> GetAWithFragment:
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=GET_A_WITH_FRAGMENT_GQL,
            operation_name="getAWithFragment",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetAWithFragment.model_validate(data)

    async def get_xyz(self, **kwargs: Any) -> GetXYZ:
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=GET_XYZ_GQL, operation_name="getXYZ", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetXYZ.model_validate(data)
