import enum
import json
from collections.abc import AsyncIterator
from typing import (
    Any,
    Optional,
    Protocol,
    TypeVar,
    Union,
    cast,
)
from uuid import uuid4

import httpx
from pydantic import BaseModel
from pydantic_core import to_jsonable_python

from .base_model import UNSET
from .exceptions import (
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


try:
    from opentelemetry.context import (  # type: ignore[import-not-found,unused-ignore]
        Context,
    )
    from opentelemetry.trace import (  # type: ignore[import-not-found,unused-ignore]
        Span,
        Tracer,
        get_tracer,
        set_span_in_context,
    )
except ImportError:
    Context = Any  # ty: ignore[invalid-assignment]
    Span = Any  # ty: ignore[invalid-assignment]
    Tracer = Any  # ty: ignore[invalid-assignment]

    def get_tracer(*args, **kwargs) -> Tracer:  # type: ignore
        raise NotImplementedError("Telemetry requires 'opentelemetry-api' package.")

    def set_span_in_context(*args, **kwargs):  # type: ignore
        raise NotImplementedError("Telemetry requires 'opentelemetry-api' package.")


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


Self = TypeVar("Self", bound="AsyncBaseClientOpenTelemetry")

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


class AsyncBaseClientOpenTelemetry:
    def __init__(
        self,
        url: str = "",
        headers: Optional[dict[str, str]] = None,
        http_client: Optional[HttpClient] = None,
        ws_url: str = "",
        ws_headers: Optional[dict[str, Any]] = None,
        ws_origin: Optional[str] = None,
        ws_connection_init_payload: Optional[dict[str, Any]] = None,
        tracer: Optional[Union[str, Tracer]] = None,
        root_context: Optional[Context] = None,
        root_span_name: str = "GraphQL Operation",
        ws_root_context: Optional[Context] = None,
        ws_root_span_name: str = "GraphQL Subscription",
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

        self.tracer: Optional[Tracer] = (
            get_tracer(tracer) if isinstance(tracer, str) else tracer
        )
        self.root_context = root_context
        self.root_span_name = root_span_name
        self.ws_root_context = ws_root_context
        self.ws_root_span_name = ws_root_span_name

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
        if self.tracer:
            return await self._execute_with_telemetry(
                query=query,
                operation_name=operation_name,
                variables=variables,
                **kwargs,
            )

        return await self._execute(
            query=query, operation_name=operation_name, variables=variables, **kwargs
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
        if self.tracer:
            generator = self._execute_ws_with_telemetry(
                query=query,
                operation_name=operation_name,
                variables=variables,
                **kwargs,
            )
        else:
            generator = self._execute_ws(
                query=query,
                operation_name=operation_name,
                variables=variables,
                **kwargs,
            )

        async for message in generator:
            yield message

    async def _execute(
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

    async def _execute_ws(
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
            # wait for connection_ack from server
            await self._handle_ws_message(
                await websocket.recv(),
                websocket,
                expected_type=GraphQLTransportWSMessageType.CONNECTION_ACK,
            )
            await self._send_subscribe(
                websocket,
                operation_id=operation_id,
                query=query,
                operation_name=operation_name,
                variables=variables,
            )

            async for message in websocket:
                data = await self._handle_ws_message(message, websocket)
                if data:
                    yield data

    async def _send_connection_init(self, websocket: ClientConnection) -> None:
        payload: dict[str, Any] = {
            "type": GraphQLTransportWSMessageType.CONNECTION_INIT.value
        }
        if self.ws_connection_init_payload:
            payload["payload"] = self.ws_connection_init_payload
        await websocket.send(json.dumps(payload))

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

        return None

    async def _execute_with_telemetry(
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Response:
        with self.tracer.start_as_current_span(  # type: ignore
            self.root_span_name, context=self.root_context
        ) as root_span:
            root_span.set_attribute("component", "GraphQL Client")

            processed_variables = (
                self._convert_dict_to_json_serializable(variables) if variables else {}
            )

            return await self._execute_json_with_telemetry(
                root_span=root_span,
                query=query,
                operation_name=operation_name,
                variables=processed_variables,
                **kwargs,
            )

    async def _execute_json_with_telemetry(
        self,
        root_span: Span,
        query: str,
        operation_name: Optional[str],
        variables: dict[str, Any],
        **kwargs: Any,
    ) -> Response:
        with self.tracer.start_as_current_span(  # type: ignore
            "json request", context=set_span_in_context(root_span)
        ) as span:
            span.set_attribute("component", "GraphQL Client")

            serialized_variables = json.dumps(variables, default=to_jsonable_python)

            span.set_attribute("query", query)
            span.set_attribute("operationName", operation_name or "")
            span.set_attribute("variables", serialized_variables)
            return await self._execute_json(
                query=query,
                operation_name=operation_name,
                variables=variables,
                **kwargs,
            )

    async def _execute_ws_with_telemetry(
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        with self.tracer.start_as_current_span(  # type: ignore
            self.ws_root_span_name, context=self.ws_root_context
        ) as root_span:
            root_span.set_attribute("component", "GraphQL Client")

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
                await self._send_connection_init_with_telemetry(
                    root_span=root_span,
                    websocket=websocket,
                )
                # wait for connection_ack from server
                await self._handle_ws_message_with_telemetry(
                    root_span=root_span,
                    message=await websocket.recv(),
                    websocket=websocket,
                    expected_type=GraphQLTransportWSMessageType.CONNECTION_ACK,
                )
                await self._send_subscribe_with_telemetry(
                    root_span=root_span,
                    websocket=websocket,
                    operation_id=operation_id,
                    query=query,
                    operation_name=operation_name,
                    variables=variables,
                )

                async for message in websocket:
                    data = await self._handle_ws_message_with_telemetry(
                        root_span=root_span, message=message, websocket=websocket
                    )
                    if data:
                        yield data

    async def _send_connection_init_with_telemetry(
        self, root_span: Span, websocket: ClientConnection
    ) -> None:
        with self.tracer.start_as_current_span(  # type: ignore
            "connection init", context=set_span_in_context(root_span)
        ) as span:
            span.set_attribute("component", "GraphQL Client")
            span.set_attribute(
                "type", GraphQLTransportWSMessageType.CONNECTION_INIT.value
            )
            if self.ws_connection_init_payload:
                span.set_attribute(
                    "payload", json.dumps(self.ws_connection_init_payload)
                )

            await self._send_connection_init(websocket=websocket)

    async def _send_subscribe_with_telemetry(
        self,
        root_span: Span,
        websocket: ClientConnection,
        operation_id: str,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[dict[str, Any]] = None,
    ) -> None:
        with self.tracer.start_as_current_span(  # type: ignore
            "subscribe", context=set_span_in_context(root_span)
        ) as span:
            span.set_attribute("component", "GraphQL Client")
            span.set_attribute("id", operation_id)
            span.set_attribute("type", GraphQLTransportWSMessageType.SUBSCRIBE.value)
            span.set_attribute("query", query)
            span.set_attribute("operationName", operation_name or "")
            if variables:
                span.set_attribute(
                    "variables",
                    json.dumps(self._convert_dict_to_json_serializable(variables)),
                )

            await self._send_subscribe(
                websocket=websocket,
                operation_id=operation_id,
                query=query,
                operation_name=operation_name,
                variables=variables,
            )

    async def _handle_ws_message_with_telemetry(
        self,
        root_span: Span,
        message: Data,
        websocket: ClientConnection,
        expected_type: Optional[GraphQLTransportWSMessageType] = None,
    ) -> Optional[dict[str, Any]]:
        with self.tracer.start_as_current_span(  # type: ignore
            "received message", context=set_span_in_context(root_span)
        ) as span:
            span.set_attribute("component", "GraphQL Client")

            try:
                message_dict = json.loads(message)
            except json.JSONDecodeError as exc:
                raise GraphQLClientInvalidMessageFormat(message=message) from exc

            type_ = message_dict.get("type")
            payload = message_dict.get("payload", {})

            span.set_attribute("type", type_)

            if not type_ or type_ not in {
                t.value for t in GraphQLTransportWSMessageType
            }:
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

            return None
