from typing import Any, Optional

import httpx
from pydantic import BaseModel

from .exceptions import GraphQLMultiError


class BaseClient:
    def __init__(
        self, base_url: str, http_client: Optional[httpx.Client] = None
    ) -> None:
        self.base_url = base_url
        self.http_client = (
            http_client if http_client else httpx.Client(base_url=base_url)
        )

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> None:
        self.http_client.close()

    def execute(
        self, query: str, variables: Optional[dict[str, Any]] = None
    ) -> httpx.Response:
        payload: dict[str, Any] = {"query": query}
        if variables:
            payload["variables"] = self._convert_dict_to_json_serializable(variables)
        return self.http_client.post(url="/graphql/", json=payload)

    def raise_for_errors(self, response: httpx.Response) -> None:
        if errors := response.json().get("errors"):
            raise GraphQLMultiError.from_errors_dicts(errors)

    def _convert_dict_to_json_serializable(self, dict_: dict[str, Any]):
        return {
            key: value
            if not isinstance(value, BaseModel)
            else value.dict(by_alias=True)
            for key, value in dict_.items()
        }
