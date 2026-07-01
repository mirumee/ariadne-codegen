import asyncio
import enum
import json
from collections.abc import AsyncIterator
from typing import Any, Optional, Protocol, TypeVar, cast
from uuid import uuid4

import httpx
from pydantic import BaseModel
from pydantic_core import to_jsonable_python

from .base_model import UNSET
from .exceptions import (
    GraphQLClientError,
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQLClientInvalidMessageFormat,
    GraphQLClientInvalidResponseError,
)

try:
    from websockets import (  # type: ignore[import-not-found,unused-ignore]
        ClientConnection,
    )
    from websockets import (  # type: ignore[import-not-found,unused-ignore]
        connect as ws_connect,
    )
    from websockets.typing import (  # type: ignore[import-not-found,unused-ignore]
        Data,
        Origin,
        Subprotocol,
    )
except ImportError:
    from contextlib import asynccontextmanager

    @asynccontextmanager  # type: ignore
    async def ws_connect(*args, **kwargs):
        raise NotImplementedError("Subscriptions require 'websockets' package.")
        yield

    ClientConnection = Any  # ty: ignore[invalid-assignment]
    Data = Any  # ty: ignore[invalid-assignment]
    Origin = Any  # ty: ignore[invalid-assignment]

    def Subprotocol(*args, **kwargs):  # type: ignore # noqa: N802, N803
        raise NotImplementedError("Subscriptions require 'websockets' package.")


class Response(Protocol):
    status_code: int

    def json(self, **kwargs: Any) -> Any: ...


class HttpClient(Protocol):
    async def post(
        self,
        url: Any | str,
        json: Any | None = None,
        data: Any | None = None,
        files: Any | None = None,
        headers: Any | None = None,
        **kwargs: Any,
    ) -> Response: ...

    async def aclose(self) -> None: ...


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
        headers: Optional[dict[str, str]] = None,
        http_client: Optional[HttpClient] = None,
        ws_url: str = "",
        ws_headers: Optional[dict[str, Any]] = None,
        ws_origin: Optional[str] = None,
        ws_connection_init_payload: Optional[dict[str, Any]] = None,
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
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Response:
        processed_variables = (
            self._convert_dict_to_json_serializable(variables) if variables else {}
        )
        return await self._execute_json(
            query=query,
            operation_name=operation_name,
            variables=processed_variables,
            **kwargs,
        )

    def get_data(self, response: Response) -> dict[str, Any]:
        if not (200 <= response.status_code <= 299):
            raise GraphQLClientHttpError(
                status_code=response.status_code, response=response
            )

        try:
            response_json = response.json()
        except ValueError as exc:
            raise GraphQLClientInvalidResponseError(response=response) from exc

        if (not isinstance(response_json, dict)) or (
            "data" not in response_json and "errors" not in response_json
        ):
            raise GraphQLClientInvalidResponseError(response=response)

        data = response_json.get("data")
        errors = response_json.get("errors")

        if errors:
            raise GraphQLClientGraphQLMultiError.from_errors_dicts(
                errors_dicts=errors, data=data
            )

        return cast(dict[str, Any], data)

    async def execute_ws(
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        headers = self.ws_headers.copy()
        headers.update(kwargs.pop("additional_headers", {}))

        merged_kwargs: dict[str, Any] = {"origin": self.ws_origin}
        merged_kwargs.update(kwargs)
        merged_kwargs["additional_headers"] = headers

        operation_id = str(uuid4())
        async with ws_connect(
            self.ws_url,
            subprotocols=[Subprotocol(GRAPHQL_TRANSPORT_WS)],
            **merged_kwargs,
        ) as websocket:
            await self._send_connection_init(websocket)
            # Wait for connection_ack; some servers (e.g. Hasura) send ping before
            # connection_ack, so we loop and handle pings until we get ack.
            try:
                await asyncio.wait_for(
                    self._wait_for_connection_ack(websocket),
                    timeout=5.0,
                )
            except asyncio.TimeoutError as exc:
                raise GraphQLClientError(
                    "Connection ack not received within 5 seconds"
                ) from exc
            await self._send_subscribe(
                websocket,
                operation_id=operation_id,
                query=query,
                operation_name=operation_name,
                variables=variables,
            )

            async for message in websocket:
                data = await self._handle_ws_message(message, websocket)
                if data and "connection_ack" not in data:
                    yield data

    def _convert_dict_to_json_serializable(
        self, dict_: dict[str, Any]
    ) -> dict[str, Any]:
        return {
            key: self._convert_value(value)
            for key, value in dict_.items()
            if value is not UNSET
        }

    def _convert_value(self, value: Any) -> Any:
        if isinstance(value, BaseModel):
            return value.model_dump(by_alias=True, exclude_unset=True)
        if isinstance(value, list):
            return [self._convert_value(item) for item in value]
        return value

    async def _execute_json(
        self,
        query: str,
        operation_name: Optional[str],
        variables: dict[str, Any],
        **kwargs: Any,
    ) -> Response:
        return await self.http_client.post(
            url=self.url,
            json=to_jsonable_python(
                {
                    "query": query,
                    "operationName": operation_name,
                    "variables": variables,
                }
            ),
            **kwargs,
        )

    async def _send_connection_init(self, websocket: ClientConnection) -> None:
        payload: dict[str, Any] = {
            "type": GraphQLTransportWSMessageType.CONNECTION_INIT.value
        }
        if self.ws_connection_init_payload:
            payload["payload"] = self.ws_connection_init_payload
        await websocket.send(json.dumps(payload))

    async def _wait_for_connection_ack(self, websocket: ClientConnection) -> None:
        """Read messages until connection_ack; handle ping/pong in between."""
        async for message in websocket:
            data = await self._handle_ws_message(message, websocket)
            if data is not None and "connection_ack" in data:
                return

    async def _send_subscribe(
        self,
        websocket: ClientConnection,
        operation_id: str,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[dict[str, Any]] = None,
    ) -> None:
        payload_inner: dict[str, Any] = {
            "query": query,
            "operationName": operation_name,
        }
        if variables:
            payload_inner["variables"] = self._convert_dict_to_json_serializable(
                variables
            )
        payload: dict[str, Any] = {
            "id": operation_id,
            "type": GraphQLTransportWSMessageType.SUBSCRIBE.value,
            "payload": payload_inner,
        }
        await websocket.send(json.dumps(payload))

    async def _handle_ws_message(
        self,
        message: Data,
        websocket: ClientConnection,
        expected_type: Optional[GraphQLTransportWSMessageType] = None,
    ) -> Optional[dict[str, Any]]:
        try:
            message_dict = json.loads(message)
        except json.JSONDecodeError as exc:
            raise GraphQLClientInvalidMessageFormat(message=message) from exc

        type_ = message_dict.get("type")
        payload = message_dict.get("payload", {})

        if not type_ or type_ not in {t.value for t in GraphQLTransportWSMessageType}:
            raise GraphQLClientInvalidMessageFormat(message=message)

        if expected_type and expected_type != type_:
            raise GraphQLClientInvalidMessageFormat(
                f"Invalid message received. Expected: {expected_type.value}"
            )

        if type_ == GraphQLTransportWSMessageType.NEXT:
            if "data" not in payload:
                raise GraphQLClientInvalidMessageFormat(message=message)
            return cast(dict[str, Any], payload["data"])

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
        elif type_ == GraphQLTransportWSMessageType.CONNECTION_ACK:
            return {"connection_ack": True}

        return None
