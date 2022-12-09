from __future__ import annotations

from typing import Any, Optional

import httpx
from pydantic import BaseModel


class BaseClient:
    def __init__(
        self, base_url: str, http_client: Optional[httpx.AsyncClient] = None
    ) -> None:
        self.base_url = base_url
        self.http_client = (
            http_client if http_client else httpx.AsyncClient(base_url=base_url)
        )

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> None:
        await self.http_client.aclose()

    async def execute(
        self, query: str, variables: Optional[dict[str, Any]] = None
    ) -> httpx.Response:
        payload: dict[str, Any] = {"query": query}
        if variables:
            payload["variables"] = self._convert_dict_to_json_serializable(variables)
        return await self.http_client.post(url="/graphql/", json=payload)

    def _convert_dict_to_json_serializable(self, dict_: dict[str, Any]):
        return {
            key: value
            if not isinstance(value, BaseModel)
            else value.dict(by_alias=True)
            for key, value in dict_.items()
        }
