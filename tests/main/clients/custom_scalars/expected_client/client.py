from datetime import datetime
from typing import Any, List, Optional

from .async_base_client import AsyncBaseClient
from .custom_scalars import Code, parse_code, serialize_code
from .get_test import GetTest
from .input_types import TestInput


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def get_test(
        self, date: datetime, code: Code, id: int, input: TestInput, other: Any
    ) -> GetTest:
        query = gql(
            """
            query getTest($date: DATETIME!, $code: CODE!, $id: CUSTOMID!, $input: TestInput!, $other: NOTMAPPED!) {
              testQuery(date: $date, code: $code, id: $id, input: $input, other: $other) {
                date
                code
                id
                other
              }
            }
            """
        )
        variables: dict[str, object] = {
            "date": date,
            "code": serialize_code(code),
            "id": id,
            "input": input,
            "other": other,
        }
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetTest.parse_obj(data)
