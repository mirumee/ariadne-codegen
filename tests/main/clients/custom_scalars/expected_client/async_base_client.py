from typing import Any, Dict, Optional, TypeVar, cast

import httpx
from pydantic import BaseModel

from .base_model import UNSET
from .exceptions import (
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQlClientInvalidResponseError,
)

Self = TypeVar("Self", bound="AsyncBaseClient")


class AsyncBaseClient:
    def __init__(
        self,
        url: str = "",
        headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self.url = url
        self.headers = headers

        self.http_client = (
            http_client if http_client else httpx.AsyncClient(headers=headers)
        )

    async def __aenter__(self: Self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: object,
        exc_val: object,
        exc_tb: object,
    ) -> None:
        await self.http_client.aclose()

    async def execute(
        self, query: str, variables: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        payload: Dict[str, Any] = {"query": query}
        if variables:
            payload["variables"] = self._convert_dict_to_json_serializable(variables)
        return await self.http_client.post(url=self.url, json=payload)

    def get_data(self, response: httpx.Response) -> dict[str, Any]:
        if not response.is_success:
            raise GraphQLClientHttpError(
                status_code=response.status_code, response=response
            )

        try:
            response_json = response.json()
        except ValueError as exc:
            raise GraphQlClientInvalidResponseError(response=response) from exc

        if (not isinstance(response_json, dict)) or ("data" not in response_json):
            raise GraphQlClientInvalidResponseError(response=response)

        data = response_json["data"]
        errors = response_json.get("errors")

        if errors:
            raise GraphQLClientGraphQLMultiError.from_errors_dicts(
                errors_dicts=errors, data=data
            )

        return cast(dict[str, Any], data)

    def _convert_value(self, value: Any) -> Any:
        if isinstance(value, BaseModel):
            return value.dict(by_alias=True, exclude_unset=True)
        if isinstance(value, list):
            return [self._convert_value(item) for item in value]
        return value

    def _convert_dict_to_json_serializable(
        self, dict_: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            key: self._convert_value(value)
            for key, value in dict_.items()
            if value is not UNSET
        }
