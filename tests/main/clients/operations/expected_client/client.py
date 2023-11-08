from typing import Any, AsyncIterator, Dict

from .async_base_client import AsyncBaseClient
from .c_mutation import CMutation
from .c_query import CQuery
from .c_subscription import CSubscription
from .custom_operations import (
    cMutation_GQL,
    cQuery_GQL,
    cSubscription_GQL,
    getA_GQL,
    getAWithFragment_GQL,
    getXYZ_GQL,
)
from .get_a import GetA
from .get_a_with_fragment import GetAWithFragment
from .get_xyz import GetXYZ


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def c_query(self, **kwargs: Any) -> CQuery:
        variables: Dict[str, object] = {}
        response = await self.execute(query=cQuery_GQL, variables=variables, **kwargs)
        data = self.get_data(response)
        return CQuery.model_validate(data)

    async def c_mutation(self, **kwargs: Any) -> CMutation:
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=cMutation_GQL, variables=variables, **kwargs
        )
        data = self.get_data(response)
        return CMutation.model_validate(data)

    async def c_subscription(self, **kwargs: Any) -> AsyncIterator[CSubscription]:
        variables: Dict[str, object] = {}
        async for data in self.execute_ws(
            query=cSubscription_GQL, variables=variables, **kwargs
        ):
            yield CSubscription.model_validate(data)

    async def get_a(self, **kwargs: Any) -> GetA:
        variables: Dict[str, object] = {}
        response = await self.execute(query=getA_GQL, variables=variables, **kwargs)
        data = self.get_data(response)
        return GetA.model_validate(data)

    async def get_a_with_fragment(self, **kwargs: Any) -> GetAWithFragment:
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=getAWithFragment_GQL, variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetAWithFragment.model_validate(data)

    async def get_xyz(self, **kwargs: Any) -> GetXYZ:
        variables: Dict[str, object] = {}
        response = await self.execute(query=getXYZ_GQL, variables=variables, **kwargs)
        data = self.get_data(response)
        return GetXYZ.model_validate(data)
