import json

import httpx
import pytest
from pydantic import BaseModel

from ariadne_codegen.generators.dependencies.async_base_client import AsyncBaseClient
from ariadne_codegen.generators.dependencies.exceptions import (
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQlClientInvalidResponseError,
)


@pytest.mark.asyncio
async def test_execute_sends_post_to_correct_endpoint_with_correct_payload(mocker):
    fake_client = mocker.AsyncMock()
    client = AsyncBaseClient(base_url="base_url", http_client=fake_client)
    query_str = """
    query Abc($v: String!) {
        abc(v: $v) {
            field1
        }
    }
    """

    await client.execute(query_str, {"v": "Xyz"})

    assert fake_client.post.called
    assert len(fake_client.post.mock_calls) == 1
    call_kwargs = fake_client.post.mock_calls[0].kwargs
    assert call_kwargs["url"] == "/graphql/"
    assert call_kwargs["json"] == {"query": query_str, "variables": {"v": "Xyz"}}


@pytest.mark.asyncio
async def test_execute_parses_pydantic_variables_before_sending(mocker):
    class TestModel1(BaseModel):
        a: int

    class TestModel2(BaseModel):
        nested: TestModel1

    fake_client = mocker.AsyncMock()
    client = AsyncBaseClient(base_url="base_url", http_client=fake_client)
    query_str = """
    query Abc($v1: TestModel1!, $v2: TestModel2) {
        abc(v1: $v1, v2: $v2){
            field1
        }
    }
    """

    await client.execute(
        query_str, {"v1": TestModel1(a=5), "v2": TestModel2(nested=TestModel1(a=10))}
    )

    assert fake_client.post.called
    assert len(fake_client.post.mock_calls) == 1
    call_kwargs = fake_client.post.mock_calls[0].kwargs
    assert call_kwargs["url"] == "/graphql/"
    assert call_kwargs["json"] == {
        "query": query_str,
        "variables": {"v1": {"a": 5}, "v2": {"nested": {"a": 10}}},
    }


@pytest.mark.parametrize(
    "status_code, response_content",
    [
        (401, {"msg": "Unauthorized"}),
        (403, {"msg": "Forbidden"}),
        (404, {"msg": "Not Found"}),
        (500, {"msg": "Internal Server Error"}),
    ],
)
def test_get_data_raises_graphql_client_http_error(
    mocker, status_code, response_content
):
    client = AsyncBaseClient(base_url="base_url", http_client=mocker.MagicMock())
    response = httpx.Response(
        status_code=status_code, content=json.dumps(response_content)
    )

    with pytest.raises(GraphQLClientHttpError) as exc:
        client.get_data(response)
        assert exc.status_code == status_code
        assert exc.response == response


@pytest.mark.parametrize("response_content", ["invalid_json", {"not_data": ""}, ""])
def test_get_data_raises_graphql_client_invalid_response_error(
    mocker, response_content
):
    client = AsyncBaseClient(base_url="base_url", http_client=mocker.MagicMock())
    response = httpx.Response(status_code=200, content=json.dumps(response_content))

    with pytest.raises(GraphQlClientInvalidResponseError) as exc:
        client.get_data(response)
        assert exc.response == response


@pytest.mark.parametrize(
    "response_content",
    [
        {
            "data": {},
            "errors": [
                {
                    "message": "Error message",
                    "locations": [{"line": 6, "column": 7}],
                    "path": ["field1", "field2", 1, "id"],
                }
            ],
        },
        {
            "data": {},
            "errors": [
                {
                    "message": "Error message type A",
                    "locations": [{"line": 6, "column": 7}],
                    "path": ["field1", "field2", 1, "id"],
                },
                {
                    "message": "Error message type B",
                    "locations": [{"line": 6, "column": 7}],
                    "path": ["field1", "field2", 1, "id"],
                },
            ],
        },
    ],
)
def test_get_data_raises_graphql_client_graphql_multi_error(mocker, response_content):
    client = AsyncBaseClient(base_url="base_url", http_client=mocker.MagicMock())

    with pytest.raises(GraphQLClientGraphQLMultiError):
        client.get_data(
            httpx.Response(status_code=200, content=json.dumps(response_content))
        )


@pytest.mark.parametrize(
    "response_content",
    [{"errors": [], "data": {}}, {"errors": None, "data": {}}, {"data": {}}],
)
def test_get_data_doesnt_raise_exception(mocker, response_content):
    client = AsyncBaseClient(base_url="base_url", http_client=mocker.MagicMock())

    data = client.get_data(
        httpx.Response(status_code=200, content=json.dumps(response_content))
    )

    assert data == response_content["data"]


@pytest.mark.asyncio
async def test_base_client_used_as_context_manager_closes_http_client(mocker):
    fake_client = mocker.AsyncMock()
    async with AsyncBaseClient(
        base_url="base_url", http_client=fake_client
    ) as base_client:
        await base_client.execute("")

    assert fake_client.aclose.called
