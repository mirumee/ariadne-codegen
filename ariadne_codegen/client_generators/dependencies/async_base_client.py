import json
from typing import Any, AsyncIterator, Dict, Optional, TypeVar, cast

import httpx
from pydantic import BaseModel
from websockets.client import WebSocketClientProtocol
from websockets.client import connect as ws_connect
from websockets.typing import Data, Subprotocol

from .base_model import UNSET
from .exceptions import (
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQLClientInvalidMessageFormat,
    GraphQlClientInvalidResponseError,
)

Self = TypeVar("Self", bound="AsyncBaseClient")

GQL_SUBPROTOCOL = "graphql-transport-ws"
GQL_CONNECTION_INIT = "connection_init"
GQL_CONNECTION_ACK = "connection_ack"
GQL_PING = "ping"
GQL_PONG = "pong"
GQL_SUBSCRIBE = "subscribe"
GQL_NEXT = "next"
GQL_ERROR = "error"
GQL_COMPLETE = "complete"


class AsyncBaseClient:
    def __init__(
        self,
        url: str = "",
        headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.AsyncClient] = None,
        connection_init_payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.url = url
        self.headers = headers
        self.http_client = (
            http_client if http_client else httpx.AsyncClient(headers=headers)
        )
        self.connection_init_payload = connection_init_payload

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
        async with ws_connect(
            self.url, subprotocols=[Subprotocol(GQL_SUBPROTOCOL)]
        ) as websocket:
            await self._send_connection_init(websocket)
            await self._send_subscribe(websocket, query=query, variables=variables)

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

    async def _send_connection_init(self, websocket: WebSocketClientProtocol):
        payload: Dict[str, Any] = {"type": GQL_CONNECTION_INIT}
        if self.connection_init_payload:
            payload["payload"] = self.connection_init_payload
        await websocket.send(json.dumps(payload))

    async def _send_subscribe(
        self,
        websocket: WebSocketClientProtocol,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
    ):
        payload: Dict[str, Any] = {"type": GQL_SUBSCRIBE, "payload": {"query": query}}
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

        if not type_ or type_ not in (
            GQL_CONNECTION_ACK,
            GQL_PING,
            GQL_PONG,
            GQL_NEXT,
            GQL_ERROR,
            GQL_COMPLETE,
        ):
            raise GraphQLClientInvalidMessageFormat(message=message)

        if type_ == GQL_NEXT:
            if "data" not in payload:
                raise GraphQLClientInvalidMessageFormat(message=message)
            return cast(Dict[str, Any], payload["data"])

        if type_ == GQL_COMPLETE:
            await websocket.close()
        elif type_ == GQL_PING:
            await websocket.send(json.dumps({"type": GQL_PONG}))
        elif type_ == GQL_ERROR:
            raise GraphQLClientGraphQLMultiError.from_errors_dicts(
                errors_dicts=payload, data=message_dict
            )

        return None
