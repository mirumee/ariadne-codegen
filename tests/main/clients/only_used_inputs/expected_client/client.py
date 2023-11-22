from typing import Any, Dict

from .async_base_client import AsyncBaseClient
from .get_a import GetA
from .get_a_2 import GetA2
from .get_b import GetB
from .input_types import InputA, InputAB


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def get_a(self, arg_a: InputA, **kwargs: Any) -> GetA:
        query = gql(
            """
            query getA($argA: InputA!) {
              a(argA: $argA)
            }
            """
        )
        variables: Dict[str, object] = {"argA": arg_a}
        response = await self.execute(query=query, variables=variables, **kwargs)
        data = self.get_data(response)
        return GetA.model_validate(data)

    async def get_a_2(self, arg_a: InputA, **kwargs: Any) -> GetA2:
        query = gql(
            """
            query getA2($argA: InputA!) {
              a(argA: $argA)
            }
            """
        )
        variables: Dict[str, object] = {"argA": arg_a}
        response = await self.execute(query=query, variables=variables, **kwargs)
        data = self.get_data(response)
        return GetA2.model_validate(data)

    async def get_b(self, arg_aa: InputAB, **kwargs: Any) -> GetB:
        query = gql(
            """
            query getB($argAA: InputAB!) {
              b(argAA: $argAA)
            }
            """
        )
        variables: Dict[str, object] = {"argAA": arg_aa}
        response = await self.execute(query=query, variables=variables, **kwargs)
        data = self.get_data(response)
        return GetB.model_validate(data)
