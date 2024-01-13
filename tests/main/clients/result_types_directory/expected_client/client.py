from typing import Any, AsyncIterator, Dict

from .async_base_client import AsyncBaseClient
from .fragments import GetQueryAFragmentQueryA
from .input_types import InputI
from .operations import (
    GET_COMPLEX_SCALAR_GQL,
    GET_QUERY_A_GQL,
    GET_QUERY_A_WITH_FRAGMENT_GQL,
    GET_QUERY_B_GQL,
    GET_QUERY_I_GQL,
    GET_QUERY_WITH_MIXINS_FRAGMENTS_GQL,
    GET_SIMPLE_SCALAR_GQL,
    SUBSCRIBE_TO_TYPE_A_GQL,
)
from .result_types.get_complex_scalar import GetComplexScalar
from .result_types.get_query_a import GetQueryA, GetQueryAQueryA
from .result_types.get_query_a_with_fragment import GetQueryAWithFragment
from .result_types.get_query_b import GetQueryB, GetQueryBQueryB
from .result_types.get_query_i import GetQueryI, GetQueryIQueryI
from .result_types.get_query_with_mixins_fragments import GetQueryWithMixinsFragments
from .result_types.get_simple_scalar import GetSimpleScalar
from .result_types.subscribe_to_type_a import (
    SubscribeToTypeA,
    SubscribeToTypeASubscribeToTypeA,
)


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def get_query_a(self, **kwargs: Any) -> GetQueryAQueryA:
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=GET_QUERY_A_GQL,
            operation_name="getQueryA",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetQueryA.model_validate(data).query_a

    async def get_query_b(self, **kwargs: Any) -> GetQueryBQueryB:
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=GET_QUERY_B_GQL,
            operation_name="getQueryB",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetQueryB.model_validate(data).query_b

    async def get_query_i(self, data_i: InputI, **kwargs: Any) -> GetQueryIQueryI:
        variables: Dict[str, object] = {"dataI": data_i}
        response = await self.execute(
            query=GET_QUERY_I_GQL,
            operation_name="getQueryI",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetQueryI.model_validate(data).query_i

    async def get_query_a_with_fragment(self, **kwargs: Any) -> GetQueryAFragmentQueryA:
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=GET_QUERY_A_WITH_FRAGMENT_GQL,
            operation_name="getQueryAWithFragment",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetQueryAWithFragment.model_validate(data).query_a

    async def get_query_with_mixins_fragments(
        self, **kwargs: Any
    ) -> GetQueryWithMixinsFragments:
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=GET_QUERY_WITH_MIXINS_FRAGMENTS_GQL,
            operation_name="getQueryWithMixinsFragments",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetQueryWithMixinsFragments.model_validate(data)

    async def get_simple_scalar(self, **kwargs: Any) -> Any:
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=GET_SIMPLE_SCALAR_GQL,
            operation_name="GetSimpleScalar",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetSimpleScalar.model_validate(data).just_simple_scalar

    async def get_complex_scalar(self, **kwargs: Any) -> Any:
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=GET_COMPLEX_SCALAR_GQL,
            operation_name="GetComplexScalar",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetComplexScalar.model_validate(data).just_complex_scalar

    async def subscribe_to_type_a(
        self, **kwargs: Any
    ) -> AsyncIterator[SubscribeToTypeASubscribeToTypeA]:
        variables: Dict[str, object] = {}
        async for data in self.execute_ws(
            query=SUBSCRIBE_TO_TYPE_A_GQL,
            operation_name="SubscribeToTypeA",
            variables=variables,
            **kwargs
        ):
            yield SubscribeToTypeA.model_validate(data).subscribe_to_type_a
