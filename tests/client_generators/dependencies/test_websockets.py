import json

import pytest

from ariadne_codegen.client_generators.dependencies.async_base_client import (
    AsyncBaseClient,
)
from ariadne_codegen.client_generators.dependencies.exceptions import (
    GraphQLClientGraphQLMultiError,
    GraphQLClientInvalidMessageFormat,
)


@pytest.fixture
def mocked_ws_connect(mocker):
    return mocker.patch(
        "ariadne_codegen.client_generators.dependencies.async_base_client.ws_connect"
    )


@pytest.fixture
def mocked_websocket(mocked_ws_connect):
    websocket = mocked_ws_connect.return_value.__aenter__.return_value
    websocket.__aiter__.return_value = [
        json.dumps({"type": "connection_ack"}),
    ]
    return websocket


@pytest.mark.asyncio
async def test_execute_ws_creates_websocket_connection_with_correct_url(
    mocked_ws_connect,
):
    async for _ in AsyncBaseClient(ws_url="ws://test_url").execute_ws(""):
        pass

    assert mocked_ws_connect.called
    assert "ws://test_url" in mocked_ws_connect.call_args.args


@pytest.mark.asyncio
async def test_execute_ws_creates_websocket_connection_with_correct_subprotocol(
    mocked_ws_connect,
):
    async for _ in AsyncBaseClient().execute_ws(""):
        pass

    assert mocked_ws_connect.called
    assert mocked_ws_connect.call_args.kwargs["subprotocols"] == [
        "graphql-transport-ws"
    ]


@pytest.mark.asyncio
async def test_execute_ws_creates_websocket_connection_with_correct_origin(
    mocked_ws_connect,
):
    async for _ in AsyncBaseClient(ws_origin="test_origin").execute_ws(""):
        pass

    assert mocked_ws_connect.called
    assert mocked_ws_connect.call_args.kwargs["origin"] == "test_origin"


@pytest.mark.asyncio
async def test_execute_ws_creates_websocket_connection_with_correct_headers(
    mocked_ws_connect,
):
    async for _ in AsyncBaseClient(ws_headers={"test_key": "test_value"}).execute_ws(
        ""
    ):
        pass

    assert mocked_ws_connect.called
    assert mocked_ws_connect.call_args.kwargs["extra_headers"] == {
        "test_key": "test_value"
    }


@pytest.mark.asyncio
async def test_execute_ws_creates_websocket_connection_with_passed_extra_headers(
    mocked_ws_connect,
):
    async for _ in AsyncBaseClient(
        ws_headers={"Client-A": "client_value_a", "Client-B": "client_value_b"}
    ).execute_ws(
        "", extra_headers={"Client-A": "execute_value_a", "Execute-Other": "other"}
    ):
        pass

    assert mocked_ws_connect.called
    assert mocked_ws_connect.call_args.kwargs["extra_headers"] == {
        "Client-A": "execute_value_a",
        "Client-B": "client_value_b",
        "Execute-Other": "other",
    }


@pytest.mark.asyncio
async def test_execute_ws_creates_websocket_connection_with_passed_kwargs(
    mocked_ws_connect,
):
    async for _ in AsyncBaseClient().execute_ws("", open_timeout=15, close_timeout=30):
        pass

    assert mocked_ws_connect.called
    assert mocked_ws_connect.call_args.kwargs["open_timeout"] == 15
    assert mocked_ws_connect.call_args.kwargs["close_timeout"] == 30


@pytest.mark.asyncio
async def test_execute_ws_sends_correct_init_connection_data(mocked_websocket):
    async for _ in AsyncBaseClient(
        ws_connection_init_payload={"test_key": "test_value"}
    ).execute_ws(""):
        pass

    init_call, _ = mocked_websocket.send.mock_calls
    sent_data = json.loads(init_call.args[0])
    assert sent_data["type"] == "connection_init"
    assert sent_data["payload"] == {"test_key": "test_value"}


@pytest.mark.asyncio
async def test_execute_ws_sends_correct_subscribe_data(mocked_websocket):
    query_str = "query testQuery($arg: String!) { test(arg: $arg) }"
    variables = {"arg": "test_value"}

    async for _ in AsyncBaseClient().execute_ws(
        query=query_str, operation_name="testQuery", variables=variables
    ):
        pass

    _, subscribe_call = mocked_websocket.send.mock_calls
    sent_data = json.loads(subscribe_call.args[0])
    assert sent_data["type"] == "subscribe"
    assert sent_data["payload"] == {
        "query": query_str,
        "operationName": "testQuery",
        "variables": variables,
    }


@pytest.mark.asyncio
async def test_execute_ws_yields_data_for_next_message(mocked_websocket):
    mocked_websocket.__aiter__.return_value.append(
        json.dumps({"type": "next", "payload": {"data": "test_data"}})
    )

    received_data = []
    async for data in AsyncBaseClient().execute_ws(""):
        received_data.append(data)

    assert received_data == ["test_data"]


@pytest.mark.asyncio
async def test_execute_ws_yields_handles_multiple_next_messages(mocked_websocket):
    mocked_websocket.__aiter__.return_value.extend(
        [
            json.dumps({"type": "next", "payload": {"data": "A"}}),
            json.dumps({"type": "next", "payload": {"data": "B"}}),
            json.dumps({"type": "next", "payload": {"data": "C"}}),
        ]
    )

    received_data = []
    async for data in AsyncBaseClient().execute_ws(""):
        received_data.append(data)

    assert received_data == ["A", "B", "C"]


@pytest.mark.asyncio
async def test_execute_ws_closes_websocket_for_complete_message(mocked_websocket):
    mocked_websocket.__aiter__.return_value.append(json.dumps({"type": "complete"}))

    async for _ in AsyncBaseClient().execute_ws(""):
        pass

    assert mocked_websocket.close.called


@pytest.mark.asyncio
async def test_execute_ws_sends_pong_for_ping_message(mocked_websocket):
    mocked_websocket.__aiter__.return_value.append(json.dumps({"type": "ping"}))

    async for _ in AsyncBaseClient().execute_ws(""):
        pass

    pong_call = mocked_websocket.send.mock_calls[-1]
    sent_data = json.loads(pong_call.args[0])
    assert sent_data["type"] == "pong"


@pytest.mark.asyncio
async def test_execute_ws_raises_invalid_message_format_for_not_json_message(
    mocked_websocket,
):
    mocked_websocket.__aiter__.return_value.append("not_valid_json")

    with pytest.raises(GraphQLClientInvalidMessageFormat):
        async for _ in AsyncBaseClient().execute_ws(""):
            pass


@pytest.mark.asyncio
async def test_execute_ws_raises_invalid_message_format_for_message_without_type(
    mocked_websocket,
):
    mocked_websocket.__aiter__.return_value.append(json.dumps({"payload": {}}))

    with pytest.raises(GraphQLClientInvalidMessageFormat):
        async for _ in AsyncBaseClient().execute_ws(""):
            pass


@pytest.mark.asyncio
async def test_execute_ws_raises_invalid_message_format_for_message_with_invalid_type(
    mocked_websocket,
):
    mocked_websocket.__aiter__.return_value.append(json.dumps({"type": "invalid_type"}))

    with pytest.raises(GraphQLClientInvalidMessageFormat):
        async for _ in AsyncBaseClient().execute_ws(""):
            pass


@pytest.mark.asyncio
async def test_execute_ws_raises_invalid_message_format_for_next_payload_without_data(
    mocked_websocket,
):
    mocked_websocket.__aiter__.return_value.append(
        json.dumps({"type": "next", "payload": {"not_data": "A"}})
    )

    with pytest.raises(GraphQLClientInvalidMessageFormat):
        async for _ in AsyncBaseClient().execute_ws(""):
            pass


@pytest.mark.asyncio
async def test_execute_ws_raises_graphql_multi_error_for_message_with_error_type(
    mocked_websocket,
):
    mocked_websocket.__aiter__.return_value.append(
        json.dumps({"type": "error", "payload": [{"message": "error_message"}]})
    )

    with pytest.raises(GraphQLClientGraphQLMultiError):
        async for _ in AsyncBaseClient().execute_ws(""):
            pass
