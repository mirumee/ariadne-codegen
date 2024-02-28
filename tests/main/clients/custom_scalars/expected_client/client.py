from datetime import datetime
from typing import Any, Dict

from .async_base_client import AsyncBaseClient
from .custom_scalars import Code, serialize_code
from .get_a import GetA
from .input_types import TestInput


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def get_a(
        self,
        date: datetime,
        code: Code,
        id: int,
        input: TestInput,
        other: Any,
        **kwargs: Any
    ) -> GetA:
        _query = gql(
            """
            query getA($date: DATETIME!, $code: CODE!, $id: CUSTOMID!, $input: TestInput!, $other: NOTMAPPED!) {
              testQuery(date: $date, code: $code, id: $id, input: $input, other: $other) {
                date
                code
                id
                other
              }
            }
            """
        )
        _variables: Dict[str, object] = {
            "date": date,
            "code": serialize_code(code),
            "id": id,
            "input": input,
            "other": other,
        }
        _response = await self.execute(
            query=_query, operation_name="getA", variables=_variables, **kwargs
        )
        _data = self.get_data(_response)
        return GetA.model_validate(_data)
