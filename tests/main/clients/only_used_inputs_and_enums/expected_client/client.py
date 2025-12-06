from typing import Any

from .async_base_client import AsyncBaseClient
from .enums import EnumD
from .get_a import GetA
from .get_a_2 import GetA2
from .get_b import GetB
from .get_d import GetD
from .get_e import GetE
from .get_f import GetF
from .get_g import GetG
from .input_types import InputA, InputAB, InputE


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
        variables: dict[str, object] = {"argA": arg_a}
        response = await self.execute(
            query=query, operation_name="getA", variables=variables, **kwargs
        )
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
        variables: dict[str, object] = {"argA": arg_a}
        response = await self.execute(
            query=query, operation_name="getA2", variables=variables, **kwargs
        )
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
        variables: dict[str, object] = {"argAA": arg_aa}
        response = await self.execute(
            query=query, operation_name="getB", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetB.model_validate(data)

    async def get_d(self, enum_d: EnumD, **kwargs: Any) -> GetD:
        query = gql(
            """
            query getD($enumD: EnumD!) {
              d(enumD: $enumD)
            }
            """
        )
        variables: dict[str, object] = {"enumD": enum_d}
        response = await self.execute(
            query=query, operation_name="getD", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetD.model_validate(data)

    async def get_e(self, arg_e: InputE, **kwargs: Any) -> GetE:
        query = gql(
            """
            query getE($argE: InputE!) {
              e(argE: $argE)
            }
            """
        )
        variables: dict[str, object] = {"argE": arg_e}
        response = await self.execute(
            query=query, operation_name="getE", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetE.model_validate(data)

    async def get_f(self, **kwargs: Any) -> GetF:
        query = gql(
            """
            query getF {
              f {
                val
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="getF", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetF.model_validate(data)

    async def get_g(self, **kwargs: Any) -> GetG:
        query = gql(
            """
            query getG {
              g {
                ...FragmentG
              }
            }

            fragment FragmentG on TypeG {
              val
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="getG", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetG.model_validate(data)
