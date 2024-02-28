from typing import Any, Dict

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
        _query = gql(
            """
            query getA($argA: InputA!) {
              a(argA: $argA)
            }
            """
        )
        _variables: Dict[str, object] = {"argA": arg_a}
        _response = await self.execute(
            query=_query, operation_name="getA", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return GetA.model_validate(_data)

    async def get_a_2(self, arg_a: InputA, **kwargs: Any) -> GetA2:
        _query = gql(
            """
            query getA2($argA: InputA!) {
              a(argA: $argA)
            }
            """
        )
        _variables: Dict[str, object] = {"argA": arg_a}
        _response = await self.execute(
            query=_query, operation_name="getA2", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return GetA2.model_validate(_data)

    async def get_b(self, arg_aa: InputAB, **kwargs: Any) -> GetB:
        _query = gql(
            """
            query getB($argAA: InputAB!) {
              b(argAA: $argAA)
            }
            """
        )
        _variables: Dict[str, object] = {"argAA": arg_aa}
        _response = await self.execute(
            query=_query, operation_name="getB", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return GetB.model_validate(_data)

    async def get_d(self, enum_d: EnumD, **kwargs: Any) -> GetD:
        _query = gql(
            """
            query getD($enumD: EnumD!) {
              d(enumD: $enumD)
            }
            """
        )
        _variables: Dict[str, object] = {"enumD": enum_d}
        _response = await self.execute(
            query=_query, operation_name="getD", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return GetD.model_validate(_data)

    async def get_e(self, arg_e: InputE, **kwargs: Any) -> GetE:
        _query = gql(
            """
            query getE($argE: InputE!) {
              e(argE: $argE)
            }
            """
        )
        _variables: Dict[str, object] = {"argE": arg_e}
        _response = await self.execute(
            query=_query, operation_name="getE", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return GetE.model_validate(_data)

    async def get_f(self, **kwargs: Any) -> GetF:
        _query = gql(
            """
            query getF {
              f {
                val
              }
            }
            """
        )
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="getF", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return GetF.model_validate(_data)

    async def get_g(self, **kwargs: Any) -> GetG:
        _query = gql(
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
        _variables: Dict[str, object] = {}
        _response = await self.execute(
            query=_query, operation_name="getG", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return GetG.model_validate(_data)
