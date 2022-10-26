import pytest
from pydantic import BaseModel

from graphql_sdk_gen.generators.base_client import BaseClient


@pytest.mark.asyncio
async def test_execute_sends_post_to_correct_endpoint_with_correct_payload(mocker):
    fake_client = mocker.AsyncMock()
    client = BaseClient("base_url", fake_client)
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
    client = BaseClient("base_url", fake_client)
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


@pytest.mark.asyncio
async def test_base_client_used_as_context_manager_closes_http_client(mocker):
    fake_client = mocker.AsyncMock()
    async with BaseClient("base_url", fake_client) as base_client:
        await base_client.execute("")

    assert fake_client.aclose.called
