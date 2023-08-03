from typing import Any, Dict

from .async_base_client import AsyncBaseClient
from .custom_scalars import serialize_code
from .get_test import GetTest
from .input_types import TestInput
from .scalars import CODE, CUSTOMID, DATETIME


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def get_test(
        self, date: DATETIME, code: CODE, id: CUSTOMID, input: TestInput, other: Any
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
        variables: Dict[str, object] = {
            "date": date,
            "code": serialize_code(code),
            "id": id,
            "input": input,
            "other": other,
        }
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetTest.model_validate(data)
