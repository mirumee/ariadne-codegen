import asyncio
import enum
import json
from collections.abc import AsyncIterator
from enum import Enum
from io import IOBase
from typing import IO, Any, Optional, Protocol, TypeVar, Union, cast
from uuid import uuid4

import httpx
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field
from pydantic_core import to_jsonable_python


class UnsetType:
    def __bool__(self) -> bool:
        return False


UNSET = UnsetType()


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        protected_namespaces=(),
    )


class Upload:
    def __init__(self, filename: str, content: IOBase, content_type: str):
        self.filename = filename
        self.content = content
        self.content_type = content_type


class Response(Protocol):
    status_code: int


class GraphQLClientError(Exception):
    """Base exception."""


class GraphQLClientHttpError(GraphQLClientError):
    def __init__(self, status_code: int, response: Response) -> None:
        self.status_code = status_code
        self.response = response

    def __str__(self) -> str:
        return f"HTTP status code: {self.status_code}"


class GraphQLClientInvalidResponseError(GraphQLClientError):
    def __init__(self, response: Response) -> None:
        self.response = response

    def __str__(self) -> str:
        return "Invalid response format."


class GraphQLClientGraphQLError(GraphQLClientError):
    def __init__(
        self,
        message: str,
        locations: Optional[list[dict[str, int]]] = None,
        path: Optional[list[str]] = None,
        extensions: Optional[dict[str, object]] = None,
        original: Optional[dict[str, object]] = None,
    ):
        self.message = message
        self.locations = locations
        self.path = path
        self.extensions = extensions
        self.original = original

    def __str__(self) -> str:
        return self.message

    @classmethod
    def from_dict(cls, error: dict[str, Any]) -> "GraphQLClientGraphQLError":
        return cls(
            message=error["message"],
            locations=error.get("locations"),
            path=error.get("path"),
            extensions=error.get("extensions"),
            original=error,
        )


class GraphQLClientGraphQLMultiError(GraphQLClientError):
    def __init__(
        self,
        errors: list[GraphQLClientGraphQLError],
        data: Optional[dict[str, Any]] = None,
    ):
        self.errors = errors
        self.data = data

    def __str__(self) -> str:
        return "; ".join((str(e) for e in self.errors))

    @classmethod
    def from_errors_dicts(
        cls, errors_dicts: list[dict[str, Any]], data: Optional[dict[str, Any]] = None
    ) -> "GraphQLClientGraphQLMultiError":
        return cls(
            errors=[GraphQLClientGraphQLError.from_dict(e) for e in errors_dicts],
            data=data,
        )


class GraphQLClientInvalidMessageFormat(GraphQLClientError):
    def __init__(self, message: Union[str, bytes]) -> None:
        self.message = message

    def __str__(self) -> str:
        return "Invalid message format."


class Color(str, Enum):
    BLACK = "BLACK"
    WHITE = "WHITE"
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    YELLOW = "YELLOW"


class CreateUser(BaseModel):
    user_create: Optional["CreateUserUserCreate"] = Field(alias="userCreate")


class CreateUserUserCreate(BaseModel):
    id: str


CreateUser.model_rebuild()


class BasicUser(BaseModel):
    id: str
    email: str


class UserPersonalData(BaseModel):
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")


BasicUser.model_rebuild()
UserPersonalData.model_rebuild()


class GetUsersCounter(BaseModel):
    users_counter: int = Field(alias="usersCounter")


class ListAllUsers(BaseModel):
    users: list["ListAllUsersUsers"]


class ListAllUsersUsers(BaseModel):
    id: str
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
    email: str
    location: Optional["ListAllUsersUsersLocation"]


class ListAllUsersUsersLocation(BaseModel):
    country: Optional[str]


ListAllUsers.model_rebuild()
ListAllUsersUsers.model_rebuild()


class UploadFile(BaseModel):
    file_upload: bool = Field(alias="fileUpload")


try:
    from websockets import ClientConnection
    from websockets import connect as ws_connect
    from websockets.typing import Data, Origin, Subprotocol
except ImportError:
    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def ws_connect(*args, **kwargs):
        raise NotImplementedError("Subscriptions require 'websockets' package.")
        yield

    ClientConnection = Any
    Data = Any
    Origin = Any

    def Subprotocol(*args, **kwargs):
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
        self, exc_type: object, exc_val: object, exc_tb: object
    ) -> None:
        await self.http_client.aclose()

    async def execute(
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Response:
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

    def get_data(self, response: Response) -> dict[str, Any]:
        if not 200 <= response.status_code <= 299:
            raise GraphQLClientHttpError(
                status_code=response.status_code, response=response
            )
        try:
            response_json = response.json()
        except ValueError as exc:
            raise GraphQLClientInvalidResponseError(response=response) from exc
        if not isinstance(response_json, dict) or (
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
            try:
                await asyncio.wait_for(
                    self._wait_for_connection_ack(websocket), timeout=5.0
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

    def _process_variables(
        self, variables: Optional[dict[str, Any]]
    ) -> tuple[
        dict[str, Any], dict[str, tuple[str, IO[bytes], str]], dict[str, list[str]]
    ]:
        if not variables:
            return ({}, {}, {})
        serializable_variables = self._convert_dict_to_json_serializable(variables)
        return self._get_files_from_variables(serializable_variables)

    def _convert_dict_to_json_serializable(
        self, dict_: dict[str, Any]
    ) -> dict[str, Any]:
        return {
            key: self._convert_value(value)
            for key, value in dict_.items()
            if value is not UNSET
        }

    def _convert_value(self, value: Any) -> Any:
        if isinstance(value, PydanticBaseModel):
            return value.model_dump(by_alias=True, exclude_unset=True)
        if isinstance(value, list):
            return [self._convert_value(item) for item in value]
        return value

    def _get_files_from_variables(
        self, variables: dict[str, Any]
    ) -> tuple[
        dict[str, Any], dict[str, tuple[str, IO[bytes], str]], dict[str, list[str]]
    ]:
        files_map: dict[str, list[str]] = {}
        files_list: list[Upload] = []

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
        files: dict[str, tuple[str, IO[bytes], str]] = {
            str(i): (file_.filename, cast(IO[bytes], file_.content), file_.content_type)
            for i, file_ in enumerate(files_list)
        }
        return (nulled_variables, files, files_map)

    async def _execute_multipart(
        self,
        query: str,
        operation_name: Optional[str],
        variables: dict[str, Any],
        files: dict[str, tuple[str, IO[bytes], str]],
        files_map: dict[str, list[str]],
        **kwargs: Any,
    ) -> Response:
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


class UserCreateInput(BaseModel):
    first_name: Optional[str] = Field(alias="firstName", default=None)
    last_name: Optional[str] = Field(alias="lastName", default=None)
    email: str
    favourite_color: Optional[Color] = Field(alias="favouriteColor", default=None)
    location: Optional["LocationInput"] = None


class LocationInput(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None


class UserPreferencesInput(BaseModel):
    lucky_number: Optional[int] = Field(alias="luckyNumber", default=7)
    favourite_word: Optional[str] = Field(alias="favouriteWord", default="word")
    color_opacity: Optional[float] = Field(alias="colorOpacity", default=1.0)
    excluded_tags: Optional[list[str]] = Field(
        alias="excludedTags", default_factory=lambda: ["offtop", "tag123"]
    )
    notifications_preferences: "NotificationsPreferencesInput" = Field(
        alias="notificationsPreferences",
        default_factory=lambda: globals()[
            "NotificationsPreferencesInput"
        ].model_validate(
            {
                "receiveMails": True,
                "receivePushNotifications": True,
                "receiveSms": False,
                "title": "Mr",
            }
        ),
    )


class NotificationsPreferencesInput(BaseModel):
    receive_mails: bool = Field(alias="receiveMails")
    receive_push_notifications: bool = Field(alias="receivePushNotifications")
    receive_sms: bool = Field(alias="receiveSms")
    title: str


class BuiltinsInput(BaseModel):
    list_: Optional[list[int]] = Field(alias="list", default=None)
    dict_: Optional[str] = Field(alias="dict", default=None)
    set_: Optional[bool] = Field(alias="set", default=None)
    tuple_: Optional[float] = Field(alias="tuple", default=None)
    int_: Optional[int] = Field(alias="int", default=None)
    str_: Optional[str] = Field(alias="str", default=None)
    bool_: Optional[bool] = Field(alias="bool", default=None)


UserCreateInput.model_rebuild()
UserPreferencesInput.model_rebuild()


class ListUsersByCountry(BaseModel):
    users: list["ListUsersByCountryUsers"]


class ListUsersByCountryUsers(BasicUser, UserPersonalData):
    favourite_color: Optional[Color] = Field(alias="favouriteColor")


ListUsersByCountry.model_rebuild()


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def create_user(
        self, user_data: UserCreateInput, **kwargs: Any
    ) -> CreateUser:
        query = gql("""
            mutation CreateUser($userData: UserCreateInput!) {
                          userCreate(userData: $userData) {
                            id
                          }
                        }
            """)
        variables: dict[str, object] = {"userData": user_data}
        response = await self.execute(
            query=query, operation_name="CreateUser", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return CreateUser.model_validate(data)

    async def list_all_users(self, **kwargs: Any) -> ListAllUsers:
        query = gql("""
            query ListAllUsers {
                          users {
                            id
                            firstName
                            lastName
                            email
                            location {
                              country
                            }
                          }
                        }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="ListAllUsers", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return ListAllUsers.model_validate(data)

    async def list_users_by_country(
        self, country: Union[Optional[str], UnsetType] = UNSET, **kwargs: Any
    ) -> ListUsersByCountry:
        query = gql("""
            query ListUsersByCountry($country: String) {
                          users(country: $country) {
                            ...BasicUser
                            ...UserPersonalData
                            favouriteColor
                          }
                        }

                        fragment BasicUser on User {
                          id
                          email
                        }

                        fragment UserPersonalData on User {
                          firstName
                          lastName
                        }
            """)
        variables: dict[str, object] = {"country": country}
        response = await self.execute(
            query=query,
            operation_name="ListUsersByCountry",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return ListUsersByCountry.model_validate(data)

    async def get_users_counter(self, **kwargs: Any) -> AsyncIterator[GetUsersCounter]:
        query = gql("""
            subscription GetUsersCounter {
                          usersCounter
                        }
            """)
        variables: dict[str, object] = {}
        async for data in self.execute_ws(
            query=query, operation_name="GetUsersCounter", variables=variables, **kwargs
        ):
            yield GetUsersCounter.model_validate(data)

    async def upload_file(self, file: Upload, **kwargs: Any) -> UploadFile:
        query = gql("""
            mutation uploadFile($file: Upload!) {
                          fileUpload(file: $file)
                        }
            """)
        variables: dict[str, object] = {"file": file}
        response = await self.execute(
            query=query, operation_name="uploadFile", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return UploadFile.model_validate(data)
