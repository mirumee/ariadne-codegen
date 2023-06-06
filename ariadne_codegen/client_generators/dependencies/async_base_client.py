import enum
import json
from typing import Any, AsyncIterator, Dict, Optional, TypeVar, cast
from uuid import uuid4

import httpx
from pydantic import BaseModel
from pydantic.json import pydantic_encoder

from .base_model import UNSET
from .exceptions import (
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQLClientInvalidMessageFormat,
    GraphQlClientInvalidResponseError,
)

try:
    from websockets.client import WebSocketClientProtocol
    from websockets.client import connect as ws_connect
    from websockets.typing import Data, Origin, Subprotocol
except ImportError:
    from contextlib import asynccontextmanager

    @asynccontextmanager  # type: ignore
    async def ws_connect(*args, **kwargs):  # pylint: disable=unused-argument
        raise NotImplementedError("Subscriptions require 'websockets' package.")
        yield  # pylint: disable=unreachable

    WebSocketClientProtocol = Any  # type: ignore
    Data = Any  # type: ignore
    Origin = Any  # type: ignore
    Subprotocol = Any  # type: ignore


Self = TypeVar("Self", bound="AsyncBaseClient")

GRAPHQL_TRANSPORT_WS = "graphql-transport-ws"


class GraphQLTransportWSMessageType(str, enum.Enum):
    CONNECTION_INIT = "connection_init"
    CONNECTION_ACK = "connection_ack"
    PING = "ping"
    PONG = "pong"
    SUBSCRIBE = "subscribe"
    NEXT = "next"
    ERROR = "error"
    COMPLETE = "complete"


class AsyncBaseClient:
    def __init__(
        self,
        url: str = "",
        headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.AsyncClient] = None,
        ws_url: str = "",
        ws_headers: Optional[Dict[str, Any]] = None,
        ws_origin: Optional[str] = None,
        ws_connection_init_payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.url = url
        self.headers = headers
        self.http_client = (
            http_client if http_client else httpx.AsyncClient(headers=headers)
        )
        self.ws_url = ws_url
        self.ws_headers = ws_headers or {}
        self.ws_origin = Origin(ws_origin) if ws_origin else None
        self.ws_connection_init_payload = ws_connection_init_payload

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
        content = json.dumps(payload, default=pydantic_encoder)
        return await self.http_client.post(
            url=self.url, content=content, headers={"Content-Type": "application/json"}
        )

    def get_data(self, response: httpx.Response) -> Dict[str, Any]:
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

    async def execute_ws(
        self, query: str, variables: Optional[Dict[str, Any]] = None
    ) -> AsyncIterator[Dict[str, Any]]:
        operation_id = str(uuid4())
        async with ws_connect(
            self.ws_url,
            subprotocols=[Subprotocol(GRAPHQL_TRANSPORT_WS)],
            origin=self.ws_origin,
            extra_headers=self.ws_headers,
        ) as websocket:
            await self._send_connection_init(websocket)
            await self._send_subscribe(
                websocket,
                operation_id=operation_id,
                query=query,
                variables=variables,
            )

            async for message in websocket:
                data = await self._handle_ws_message(message, websocket)
                if data:
                    yield data

    def _convert_dict_to_json_serializable(
        self, dict_: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            key: self._convert_value(value)
            for key, value in dict_.items()
            if value is not UNSET
        }

    def _convert_value(self, value: Any) -> Any:
        if isinstance(value, BaseModel):
            return value.dict(by_alias=True, exclude_unset=True)
        if isinstance(value, list):
            return [self._convert_value(item) for item in value]
        return value

    async def _send_connection_init(self, websocket: WebSocketClientProtocol) -> None:
        payload: Dict[str, Any] = {
            "type": GraphQLTransportWSMessageType.CONNECTION_INIT.value
        }
        if self.ws_connection_init_payload:
            payload["payload"] = self.ws_connection_init_payload
        await websocket.send(json.dumps(payload))

    async def _send_subscribe(
        self,
        websocket: WebSocketClientProtocol,
        operation_id: str,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
    ) -> None:
        payload: Dict[str, Any] = {
            "id": operation_id,
            "type": GraphQLTransportWSMessageType.SUBSCRIBE.value,
            "payload": {"query": query},
        }
        if variables:
            payload["payload"]["variables"] = self._convert_dict_to_json_serializable(
                variables
            )
        await websocket.send(json.dumps(payload))

    async def _handle_ws_message(
        self, message: Data, websocket: WebSocketClientProtocol
    ) -> Optional[Dict[str, Any]]:
        try:
            message_dict = json.loads(message)
        except json.JSONDecodeError as exc:
            raise GraphQLClientInvalidMessageFormat(message=message) from exc

        type_ = message_dict.get("type")
        payload = message_dict.get("payload", {})

        if not type_ or type_ not in {t.value for t in GraphQLTransportWSMessageType}:
            raise GraphQLClientInvalidMessageFormat(message=message)

        if type_ == GraphQLTransportWSMessageType.NEXT:
            if "data" not in payload:
                raise GraphQLClientInvalidMessageFormat(message=message)
            return cast(Dict[str, Any], payload["data"])

        if type_ == GraphQLTransportWSMessageType.COMPLETE:
            await websocket.close()
        elif type_ == GraphQLTransportWSMessageType.PING:
            await websocket.send(
                json.dumps({"type": GraphQLTransportWSMessageType.PONG.value})
            )
        elif type_ == GraphQLTransportWSMessageType.ERROR:
            raise GraphQLClientGraphQLMultiError.from_errors_dicts(
                errors_dicts=payload, data=message_dict
            )

        return None
