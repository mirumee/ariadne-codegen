from collections.abc import AsyncIterator
from typing import Any

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
    GET_S_GQL,
    GET_XYZ_GQL,
)
from .get_a import GetA
from .get_a_with_fragment import GetAWithFragment
from .get_s import GetS
from .get_xyz import GetXYZ


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def c_query(self, **kwargs: Any) -> CQuery:
        variables: dict[str, object] = {}
        response = await self.execute(
            query=C_QUERY_GQL, operation_name="cQuery", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return CQuery.model_validate(data)

    async def c_mutation(self, **kwargs: Any) -> CMutation:
        variables: dict[str, object] = {}
        response = await self.execute(
            query=C_MUTATION_GQL,
            operation_name="cMutation",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return CMutation.model_validate(data)

    async def c_subscription(self, **kwargs: Any) -> AsyncIterator[CSubscription]:
        variables: dict[str, object] = {}
        async for data in self.execute_ws(
            query=C_SUBSCRIPTION_GQL,
            operation_name="cSubscription",
            variables=variables,
            **kwargs
        ):
            yield CSubscription.model_validate(data)

    async def get_a(self, **kwargs: Any) -> GetA:
        variables: dict[str, object] = {}
        response = await self.execute(
            query=GET_A_GQL, operation_name="getA", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetA.model_validate(data)

    async def get_a_with_fragment(self, **kwargs: Any) -> GetAWithFragment:
        variables: dict[str, object] = {}
        response = await self.execute(
            query=GET_A_WITH_FRAGMENT_GQL,
            operation_name="getAWithFragment",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetAWithFragment.model_validate(data)

    async def get_xyz(self, **kwargs: Any) -> GetXYZ:
        variables: dict[str, object] = {}
        response = await self.execute(
            query=GET_XYZ_GQL, operation_name="getXYZ", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetXYZ.model_validate(data)

    async def get_s(self, **kwargs: Any) -> GetS:
        variables: dict[str, object] = {}
        response = await self.execute(
            query=GET_S_GQL, operation_name="getS", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetS.model_validate(data)
