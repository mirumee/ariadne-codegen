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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=C_QUERY_GQL, operation_name="cQuery", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return CQuery.model_validate(_data)

    async def c_mutation(self, **kwargs: Any) -> CMutation:
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=C_MUTATION_GQL,
            operation_name="cMutation",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return CMutation.model_validate(_data)

    async def c_subscription(self, **kwargs: Any) -> AsyncIterator[CSubscription]:
        _variables: Dict[str, object] = {}
        async for _data in self.execute_ws(
            query=C_SUBSCRIPTION_GQL,
            operation_name="cSubscription",
            variables=_variables,
            **kwargs
        ):
            yield CSubscription.model_validate(_data)

    async def get_a(self, **kwargs: Any) -> GetA:
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=GET_A_GQL, operation_name="getA", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return GetA.model_validate(_data)

    async def get_a_with_fragment(self, **kwargs: Any) -> GetAWithFragment:
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=GET_A_WITH_FRAGMENT_GQL,
            operation_name="getAWithFragment",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return GetAWithFragment.model_validate(_data)

    async def get_xyz(self, **kwargs: Any) -> GetXYZ:
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=GET_XYZ_GQL, operation_name="getXYZ", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return GetXYZ.model_validate(_data)

    async def get_s(self, **kwargs: Any) -> GetS:
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=GET_S_GQL, operation_name="getS", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return GetS.model_validate(_data)
