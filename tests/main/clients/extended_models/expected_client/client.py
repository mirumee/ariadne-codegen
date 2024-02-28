from typing import Any, Dict

from .async_base_client import AsyncBaseClient
from .fragments_with_mixins import FragmentsWithMixins
from .get_query_a import GetQueryA
from .get_query_a_with_fragment import GetQueryAWithFragment
from .get_query_b import GetQueryB


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def get_query_a(self, **kwargs: Any) -> GetQueryA:
        _query = gql(
            """
            query getQueryA {
              queryA {
                fieldA
              }
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="getQueryA", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return GetQueryA.model_validate(_data)

    async def get_query_b(self, **kwargs: Any) -> GetQueryB:
        _query = gql(
            """
            query getQueryB {
              queryB {
                fieldB
              }
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="getQueryB", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return GetQueryB.model_validate(_data)

    async def get_query_a_with_fragment(self, **kwargs: Any) -> GetQueryAWithFragment:
        _query = gql(
            """
            query getQueryAWithFragment {
              ...getQueryAFragment
            }

            fragment getQueryAFragment on Query {
              queryA {
                fieldA
              }
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query,
            operation_name="getQueryAWithFragment",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return GetQueryAWithFragment.model_validate(_data)

    async def fragments_with_mixins(self, **kwargs: Any) -> FragmentsWithMixins:
        _query = gql(
            """
            query fragmentsWithMixins {
              queryA {
                ...fragmentA
              }
              queryB {
                ...fragmentB
              }
            }

            fragment fragmentA on TypeA @mixin(from: ".mixins_a", import: "MixinA") {
              fieldA
            }

            fragment fragmentB on TypeB @mixin(from: ".mixins_b", import: "MixinB") {
              fieldB
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query,
            operation_name="fragmentsWithMixins",
            variables=_variables,
            **kwargs
        )
        _data = self.get_data(_response)
        return FragmentsWithMixins.model_validate(_data)
