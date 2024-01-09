import enum
import json
from typing import (
    IO,
    Any,
    AsyncIterator,
    Dict,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
)
from uuid import uuid4

import httpx
from pydantic import BaseModel
from pydantic_core import to_jsonable_python

from .base_model import UNSET, Upload
from .exceptions import (
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQLClientInvalidMessageFormat,
    GraphQLClientInvalidResponseError,
)

try:
    from websockets.client import (  # type: ignore[import-not-found,unused-ignore]
        WebSocketClientProtocol,
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
    async def ws_connect(*args, **kwargs):  # pylint: disable=unused-argument
        raise NotImplementedError("Subscriptions require 'websockets' package.")
        yield  # pylint: disable=unreachable

    WebSocketClientProtocol = Any  # type: ignore[misc,assignment,unused-ignore]
    Data = Any  # type: ignore[misc,assignment,unused-ignore]
    Origin = Any  # type: ignore[misc,assignment,unused-ignore]

    def Subprotocol(*args, **kwargs):  # type: ignore # pylint: disable=invalid-name
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
    Context = Any  # type: ignore[misc,assignment,unused-ignore]
    Span = Any  # type: ignore[misc,assignment,unused-ignore]
    Tracer = Any  # type: ignore[misc,assignment,unused-ignore]

    def get_tracer(*args, **kwargs) -> Tracer:  # type: ignore
        raise NotImplementedError("Telemetry requires 'opentelemetry-api' package.")

    def set_span_in_context(*args, **kwargs):  # type: ignore
        raise NotImplementedError("Telemetry requires 'opentelemetry-api' package.")


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
        headers: Optional[Dict[str, str]] = None,
        http_client: Optional[httpx.AsyncClient] = None,
        ws_url: str = "",
        ws_headers: Optional[Dict[str, Any]] = None,
        ws_origin: Optional[str] = None,
        ws_connection_init_payload: Optional[Dict[str, Any]] = None,
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
        variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
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

    def get_data(self, response: httpx.Response) -> Dict[str, Any]:
        if not response.is_success:
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

        return cast(Dict[str, Any], data)

    async def execute_ws(
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> AsyncIterator[Dict[str, Any]]:
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
        variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        processed_variables, files, files_map = self._process_variables(variables)

        if files and files_map:
            return await self._execute_multipart(
                query=query,
                operation_name=operation_name,
                variables=processed_variables,
                files=files,
                files_map=files_map,
                **kwargs,
            )

        return await self._execute_json(
            query=query,
            operation_name=operation_name,
            variables=processed_variables,
            **kwargs,
        )

    def _process_variables(
        self, variables: Optional[Dict[str, Any]]
    ) -> Tuple[
        Dict[str, Any], Dict[str, Tuple[str, IO[bytes], str]], Dict[str, List[str]]
    ]:
        if not variables:
            return {}, {}, {}

        serializable_variables = self._convert_dict_to_json_serializable(variables)
        return self._get_files_from_variables(serializable_variables)

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
            return value.model_dump(by_alias=True, exclude_unset=True)
        if isinstance(value, list):
            return [self._convert_value(item) for item in value]
        return value

    def _get_files_from_variables(
        self, variables: Dict[str, Any]
    ) -> Tuple[
        Dict[str, Any], Dict[str, Tuple[str, IO[bytes], str]], Dict[str, List[str]]
    ]:
        files_map: Dict[str, List[str]] = {}
        files_list: List[Upload] = []

        def separate_files(path: str, obj: Any) -> Any:
            if isinstance(obj, list):
                nulled_list = []
                for index, value in enumerate(obj):
                    value = separate_files(f"{path}.{index}", value)
                    nulled_list.append(value)
                return nulled_list

            if isinstance(obj, dict):
                nulled_dict = {}
                for key, value in obj.items():
                    value = separate_files(f"{path}.{key}", value)
                    nulled_dict[key] = value
                return nulled_dict

            if isinstance(obj, Upload):
                if obj in files_list:
                    file_index = files_list.index(obj)
                    files_map[str(file_index)].append(path)
                else:
                    file_index = len(files_list)
                    files_list.append(obj)
                    files_map[str(file_index)] = [path]
                return None

            return obj

        nulled_variables = separate_files("variables", variables)
        files: Dict[str, Tuple[str, IO[bytes], str]] = {
            str(i): (file_.filename, cast(IO[bytes], file_.content), file_.content_type)
            for i, file_ in enumerate(files_list)
        }
        return nulled_variables, files, files_map

    async def _execute_multipart(
        self,
        query: str,
        operation_name: Optional[str],
        variables: Dict[str, Any],
        files: Dict[str, Tuple[str, IO[bytes], str]],
        files_map: Dict[str, List[str]],
        **kwargs: Any,
    ) -> httpx.Response:
        data = {
            "operations": json.dumps(
                {
                    "query": query,
                    "operationName": operation_name,
                    "variables": variables,
                },
                default=to_jsonable_python,
            ),
            "map": json.dumps(files_map, default=to_jsonable_python),
        }

        return await self.http_client.post(
            url=self.url, data=data, files=files, **kwargs
        )

    async def _execute_json(
        self,
        query: str,
        operation_name: Optional[str],
        variables: Dict[str, Any],
        **kwargs: Any,
    ) -> httpx.Response:
        headers: Dict[str, str] = {"Content-Type": "application/json"}
        headers.update(kwargs.get("headers", {}))

        merged_kwargs: Dict[str, Any] = kwargs.copy()
        merged_kwargs["headers"] = headers

        return await self.http_client.post(
            url=self.url,
            content=json.dumps(
                {
                    "query": query,
                    "operationName": operation_name,
                    "variables": variables,
                },
                default=to_jsonable_python,
            ),
            **merged_kwargs,
        )

    async def _execute_ws(
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> AsyncIterator[Dict[str, Any]]:
        headers = self.ws_headers.copy()
        headers.update(kwargs.get("extra_headers", {}))

        merged_kwargs: Dict[str, Any] = {"origin": self.ws_origin}
        merged_kwargs.update(kwargs)
        merged_kwargs["extra_headers"] = headers

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
        operation_name: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
    ) -> None:
        payload: Dict[str, Any] = {
            "id": operation_id,
            "type": GraphQLTransportWSMessageType.SUBSCRIBE.value,
            "payload": {"query": query, "operationName": operation_name},
        }
        if variables:
            payload["payload"]["variables"] = self._convert_dict_to_json_serializable(
                variables
            )
        await websocket.send(json.dumps(payload))

    async def _handle_ws_message(
        self,
        message: Data,
        websocket: WebSocketClientProtocol,
        expected_type: Optional[GraphQLTransportWSMessageType] = None,
    ) -> Optional[Dict[str, Any]]:
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

    async def _execute_with_telemetry(
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        with self.tracer.start_as_current_span(  # type: ignore
            self.root_span_name, context=self.root_context
        ) as root_span:
            root_span.set_attribute("component", "GraphQL Client")

            processed_variables, files, files_map = self._process_variables(variables)

            if files and files_map:
                return await self._execute_multipart_with_telemetry(
                    root_span=root_span,
                    query=query,
                    operation_name=operation_name,
                    variables=processed_variables,
                    files=files,
                    files_map=files_map,
                    **kwargs,
                )

            return await self._execute_json_with_telemetry(
                root_span=root_span,
                query=query,
                operation_name=operation_name,
                variables=processed_variables,
                **kwargs,
            )

    async def _execute_multipart_with_telemetry(
        self,
        root_span: Span,
        query: str,
        operation_name: Optional[str],
        variables: Dict[str, Any],
        files: Dict[str, Tuple[str, IO[bytes], str]],
        files_map: Dict[str, List[str]],
        **kwargs: Any,
    ) -> httpx.Response:
        with self.tracer.start_as_current_span(  # type: ignore
            "multipart request", context=set_span_in_context(root_span)
        ) as span:
            span.set_attribute("component", "GraphQL Client")

            serialized_variables = json.dumps(variables, default=to_jsonable_python)
            serialized_map = json.dumps(files_map, default=to_jsonable_python)

            span.set_attribute("query", query)
            span.set_attribute("operationName", operation_name or "")
            span.set_attribute("variables", serialized_variables)
            span.set_attribute("map", serialized_map)
            return await self._execute_multipart(
                query=query,
                operation_name=operation_name,
                variables=variables,
                files=files,
                files_map=files_map,
                **kwargs,
            )

    async def _execute_json_with_telemetry(
        self,
        root_span: Span,
        query: str,
        operation_name: Optional[str],
        variables: Dict[str, Any],
        **kwargs: Any,
    ) -> httpx.Response:
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
        variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> AsyncIterator[Dict[str, Any]]:
        with self.tracer.start_as_current_span(  # type: ignore
            self.ws_root_span_name, context=self.ws_root_context
        ) as root_span:
            root_span.set_attribute("component", "GraphQL Client")

            headers = self.ws_headers.copy()
            headers.update(kwargs.get("extra_headers", {}))

            merged_kwargs: Dict[str, Any] = {"origin": self.ws_origin}
            merged_kwargs.update(kwargs)
            merged_kwargs["extra_headers"] = headers

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
        self, root_span: Span, websocket: WebSocketClientProtocol
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
        websocket: WebSocketClientProtocol,
        operation_id: str,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
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
        websocket: WebSocketClientProtocol,
        expected_type: Optional[GraphQLTransportWSMessageType] = None,
    ) -> Optional[Dict[str, Any]]:
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
