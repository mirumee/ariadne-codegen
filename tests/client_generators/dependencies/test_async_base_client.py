import json
from datetime import datetime
from typing import Any, Optional

import httpx
import pytest

from ariadne_codegen.client_generators.dependencies.async_base_client import (
    AsyncBaseClient,
)
from ariadne_codegen.client_generators.dependencies.base_model import UNSET, BaseModel
from ariadne_codegen.client_generators.dependencies.exceptions import (
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQLClientInvalidResponseError,
)

from ...utils import decode_multipart_request


@pytest.mark.asyncio
async def test_execute_sends_post_to_correct_url_with_correct_payload(httpx_mock):
    httpx_mock.add_response()

    client = AsyncBaseClient(url="http://base_url/endpoint")
    query_str = """
    query Abc($v: String!) {
        abc(v: $v) {
            field1
        }
    }
    """

    await client.execute(query_str, "Abc", {"v": "Xyz"})

    request = httpx_mock.get_request()
    assert request.url == "http://base_url/endpoint"
    content = json.loads(request.content)
    assert content == {
        "query": query_str,
        "operationName": "Abc",
        "variables": {"v": "Xyz"},
    }


@pytest.mark.asyncio
async def test_execute_parses_pydantic_variables_before_sending(httpx_mock):
    class TestModel1(BaseModel):
        a: int

    class TestModel2(BaseModel):
        nested: TestModel1

    httpx_mock.add_response()
    client = AsyncBaseClient(url="http://base_url")
    query_str = """
    query Abc($v1: TestModel1!, $v2: TestModel2) {
        abc(v1: $v1, v2: $v2){
            field1
        }
    }
    """

    await client.execute(
        query_str,
        "Abc",
        {"v1": TestModel1(a=5), "v2": TestModel2(nested=TestModel1(a=10))},
    )

    request = httpx_mock.get_request()
    content = json.loads(request.content)
    assert content == {
        "query": query_str,
        "operationName": "Abc",
        "variables": {"v1": {"a": 5}, "v2": {"nested": {"a": 10}}},
    }


@pytest.mark.asyncio
async def test_execute_correctly_parses_top_level_list_variables(httpx_mock):
    class TestModel1(BaseModel):
        a: int

    httpx_mock.add_response()
    client = AsyncBaseClient(url="http://base_url")
    query_str = """
    query Abc($v1: [[TestModel1!]!]!) {
        abc(v1: $v1){
            field1
        }
    }
    """

    await client.execute(
        query_str,
        "Abc",
        {
            "v1": [[TestModel1(a=1), TestModel1(a=2)]],
        },
    )

    request = httpx_mock.get_request()
    content = json.loads(request.content)
    assert content == {
        "query": query_str,
        "operationName": "Abc",
        "variables": {"v1": [[{"a": 1}, {"a": 2}]]},
    }
    assert not any(isinstance(x, BaseModel) for x in content["variables"]["v1"][0])


@pytest.mark.asyncio
async def test_execute_sends_payload_without_unset_arguments(httpx_mock):
    httpx_mock.add_response()
    client = AsyncBaseClient(url="http://base_url")
    query_str = """
    query Abc($arg1: TestInputA, $arg2: String, $arg3: Float, $arg4: Int!) {
        abc(arg1: $arg1, arg2: $arg2, arg3: $arg3, arg4: $arg4){
            field1
        }
    }
    """

    await client.execute(
        query_str, "Abc", {"arg1": UNSET, "arg2": UNSET, "arg3": None, "arg4": 2}
    )

    request = httpx_mock.get_request()
    content = json.loads(request.content)
    assert content == {
        "query": query_str,
        "operationName": "Abc",
        "variables": {"arg3": None, "arg4": 2},
    }


@pytest.mark.asyncio
async def test_execute_sends_payload_without_unset_input_fields(httpx_mock):
    class TestInputB(BaseModel):
        required_b: str
        optional_b: Optional[str] = None

    class TestInputA(BaseModel):
        required_a: str
        optional_a: Optional[str] = None
        input_b1: Optional[TestInputB] = None
        input_b2: Optional[TestInputB] = None
        input_b3: Optional[TestInputB] = None

    httpx_mock.add_response()
    client = AsyncBaseClient(url="http://base_url")
    query_str = """
    query Abc($arg: TestInputB) {
        abc(arg: $arg){
            field1
        }
    }
    """

    await client.execute(
        query_str,
        "Abc",
        {
            "arg": TestInputA(
                required_a="a", input_b1=TestInputB(required_b="b"), input_b3=None
            )
        },
    )

    request = httpx_mock.get_request()
    content = json.loads(request.content)
    assert content == {
        "query": query_str,
        "operationName": "Abc",
        "variables": {
            "arg": {
                "required_a": "a",
                "input_b1": {"required_b": "b"},
                "input_b3": None,
            }
        },
    }


@pytest.mark.asyncio
async def test_execute_sends_payload_with_serialized_datetime_without_exception(
    httpx_mock,
):
    httpx_mock.add_response()
    client = AsyncBaseClient(url="http://base_url")
    query_str = "query Abc($arg: DATETIME) { abc }"
    arg_value = datetime(2023, 12, 31, 10, 15)

    await client.execute(query_str, "Abc", {"arg": arg_value})

    request = httpx_mock.get_request()
    content = json.loads(request.content)
    assert content["variables"]["arg"] == arg_value.isoformat()


@pytest.mark.asyncio
async def test_execute_sends_request_with_correct_content_type(httpx_mock):
    httpx_mock.add_response()
    client = AsyncBaseClient(url="http://base_url")

    await client.execute("query Abc { abc }")

    request = httpx_mock.get_request()
    assert request.headers["Content-Type"] == "application/json"


@pytest.mark.asyncio
async def test_execute_sends_request_with_extra_headers_and_correct_content_type(
    httpx_mock,
):
    httpx_mock.add_response()
    client = AsyncBaseClient(url="http://base_url", headers={"h_key": "h_value"})

    await client.execute("query Abc { abc }")

    request = httpx_mock.get_request()
    assert request.headers["h_key"] == "h_value"
    assert request.headers["Content-Type"] == "application/json"


@pytest.mark.asyncio
async def test_execute_passes_kwargs_to_json_post(mocker):
    http_client = mocker.AsyncMock()

    await AsyncBaseClient(url="http://base_url", http_client=http_client).execute(
        "query Abc { abc }", timeout=333, follow_redirects=False
    )

    assert http_client.post.call_args.kwargs["timeout"] == 333
    assert http_client.post.call_args.kwargs["follow_redirects"] is False


@pytest.mark.asyncio
async def test_execute_sends_json_request_with_headers_from_passed_kwargs(httpx_mock):
    httpx_mock.add_response()
    client = AsyncBaseClient(
        url="http://base_url",
        headers={
            "Client-Header-A": "client_value_A",
            "Client-Header-B": "client_value_b",
        },
    )

    await client.execute(
        "query Abc { abc }",
        "Abc",
        {},
        headers={"Other-Header": "other", "Client-Header-A": "execute_value"},
    )

    request = httpx_mock.get_request()
    assert request.headers["Content-Type"] == "application/json"
    assert request.headers["Other-Header"] == "other"
    assert request.headers["Client-Header-A"] == "execute_value"
    assert request.headers["Client-Header-b"] == "client_value_b"


@pytest.mark.asyncio
async def test_execute_sends_file_with_multipart_form_data_content_type(
    httpx_mock, txt_file
):
    httpx_mock.add_response()

    client = AsyncBaseClient(url="http://base_url")
    await client.execute(
        "query Abc($file: Upload!) { abc(file: $file) }", "Abc", {"file": txt_file}
    )

    request = httpx_mock.get_request()
    assert "multipart/form-data" in request.headers["Content-Type"]


@pytest.mark.asyncio
async def test_execute_sends_file_as_multipart_request(httpx_mock, txt_file):
    httpx_mock.add_response()
    query_str = "query Abc($file: Upload!) { abc(file: $file) }"

    client = AsyncBaseClient(url="http://base_url")
    await client.execute(query_str, "Abc", {"file": txt_file})

    request = httpx_mock.get_request()
    request.read()
    assert "multipart/form-data" in request.headers["Content-Type"]
    sent_parts = decode_multipart_request(request)

    assert sent_parts["operations"]
    decoded_operations = json.loads(sent_parts["operations"].content)
    assert decoded_operations == {
        "query": query_str,
        "operationName": "Abc",
        "variables": {"file": None},
    }

    assert sent_parts["map"]
    decoded_map = json.loads(sent_parts["map"].content)
    assert decoded_map == {"0": ["variables.file"]}

    assert sent_parts["0"]
    assert sent_parts["0"].headers[b"Content-Type"] == b"text/plain"
    assert b"txt_file.txt" in sent_parts["0"].headers[b"Content-Disposition"]
    assert sent_parts["0"].content == b"abcdefgh"


@pytest.mark.asyncio
async def test_execute_sends_file_from_memory(httpx_mock, in_memory_txt_file):
    httpx_mock.add_response()
    query_str = "query Abc($file: Upload!) { abc(file: $file) }"

    client = AsyncBaseClient(url="http://base_url")
    await client.execute(query_str, "Abc", {"file": in_memory_txt_file})

    request = httpx_mock.get_request()
    request.read()
    assert "multipart/form-data" in request.headers["Content-Type"]
    sent_parts = decode_multipart_request(request)

    assert sent_parts["operations"]
    decoded_operations = json.loads(sent_parts["operations"].content)
    assert decoded_operations == {
        "query": query_str,
        "operationName": "Abc",
        "variables": {"file": None},
    }

    assert sent_parts["map"]
    decoded_map = json.loads(sent_parts["map"].content)
    assert decoded_map == {"0": ["variables.file"]}

    assert sent_parts["0"]
    assert sent_parts["0"].headers[b"Content-Type"] == b"text/plain"
    assert b"in_memory.txt" in sent_parts["0"].headers[b"Content-Disposition"]
    assert sent_parts["0"].content == b"123456"


@pytest.mark.asyncio
async def test_execute_sends_multiple_files(httpx_mock, txt_file, png_file):
    httpx_mock.add_response()
    query_str = "query Abc($files: [Upload!]!) { abc(files: $files) }"

    client = AsyncBaseClient(url="http://base_url")
    await client.execute(query_str, "Abc", {"files": [txt_file, png_file]})

    request = httpx_mock.get_request()
    request.read()
    assert "multipart/form-data" in request.headers["Content-Type"]
    sent_parts = decode_multipart_request(request)

    assert sent_parts["operations"]
    decoded_operations = json.loads(sent_parts["operations"].content)
    assert decoded_operations == {
        "query": query_str,
        "operationName": "Abc",
        "variables": {"files": [None, None]},
    }

    assert sent_parts["map"]
    decoded_map = json.loads(sent_parts["map"].content)
    assert decoded_map == {"0": ["variables.files.0"], "1": ["variables.files.1"]}

    assert sent_parts["0"]
    assert sent_parts["0"].headers[b"Content-Type"] == b"text/plain"
    assert b"txt_file.txt" in sent_parts["0"].headers[b"Content-Disposition"]
    assert sent_parts["0"].content == b"abcdefgh"

    assert sent_parts["1"]
    assert sent_parts["1"].headers[b"Content-Type"] == b"image/png"
    assert b"png_file.png" in sent_parts["1"].headers[b"Content-Disposition"]
    assert sent_parts["1"].content == b"image_content"


@pytest.mark.asyncio
async def test_execute_sends_nested_file(httpx_mock, txt_file):
    class InputType(BaseModel):
        file_: Any

    httpx_mock.add_response()
    query_str = "query Abc($input: InputType!) { abc(input: $input) }"

    client = AsyncBaseClient(url="http://base_url")
    await client.execute(query_str, "Abc", {"input": InputType(file_=txt_file)})

    request = httpx_mock.get_request()
    request.read()
    assert "multipart/form-data" in request.headers["Content-Type"]
    sent_parts = decode_multipart_request(request)

    assert sent_parts["operations"]
    decoded_operations = json.loads(sent_parts["operations"].content)
    assert decoded_operations == {
        "query": query_str,
        "operationName": "Abc",
        "variables": {"input": {"file_": None}},
    }

    assert sent_parts["map"]
    decoded_map = json.loads(sent_parts["map"].content)
    assert decoded_map == {"0": ["variables.input.file_"]}

    assert sent_parts["0"]
    assert sent_parts["0"].headers[b"Content-Type"] == b"text/plain"
    assert b"txt_file.txt" in sent_parts["0"].headers[b"Content-Disposition"]
    assert sent_parts["0"].content == b"abcdefgh"


@pytest.mark.asyncio
async def test_execute_sends_each_file_only_once(httpx_mock, txt_file):
    httpx_mock.add_response()
    query_str = "query Abc($files: [Upload!]!) { abc(files: $files) }"

    client = AsyncBaseClient(url="http://base_url")
    await client.execute(query_str, "Abc", {"files": [txt_file, txt_file]})

    request = httpx_mock.get_request()
    request.read()
    assert "multipart/form-data" in request.headers["Content-Type"]
    sent_parts = decode_multipart_request(request)

    assert sent_parts["operations"]
    decoded_operations = json.loads(sent_parts["operations"].content)
    assert decoded_operations == {
        "query": query_str,
        "operationName": "Abc",
        "variables": {"files": [None, None]},
    }

    assert sent_parts["map"]
    decoded_map = json.loads(sent_parts["map"].content)
    assert decoded_map == {"0": ["variables.files.0", "variables.files.1"]}

    assert sent_parts["0"]
    assert sent_parts["0"].headers[b"Content-Type"] == b"text/plain"
    assert b"txt_file.txt" in sent_parts["0"].headers[b"Content-Disposition"]
    assert sent_parts["0"].content == b"abcdefgh"


@pytest.mark.asyncio
async def test_execute_passes_kwargs_to_multipart_post(mocker, txt_file):
    http_client = mocker.AsyncMock()

    await AsyncBaseClient(url="http://base_url", http_client=http_client).execute(
        "query Abc($file: Upload!) { abc(file: $file) }",
        "Abc",
        {"file": txt_file},
        timeout=333,
        follow_redirects=False,
    )

    assert http_client.post.call_args.kwargs["timeout"] == 333
    assert http_client.post.call_args.kwargs["follow_redirects"] is False


@pytest.mark.asyncio
async def test_execute_sends_multipart_request_with_headers_from_passed_kwargs(
    httpx_mock, txt_file
):
    httpx_mock.add_response()
    client = AsyncBaseClient(
        url="http://base_url",
        headers={
            "Client-Header-A": "client_value_A",
            "Client-Header-B": "client_value_b",
        },
    )

    await client.execute(
        "query Abc($file: Upload!) { abc(file: $file) }",
        "Abc",
        {"file": txt_file},
        headers={
            "Other-Header": "other",
            "Client-Header-A": "execute_value",
        },
    )

    request = httpx_mock.get_request()
    assert request.headers["Other-Header"] == "other"
    assert request.headers["Client-Header-A"] == "execute_value"
    assert request.headers["Client-Header-B"] == "client_value_b"


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
    client = AsyncBaseClient(url="base_url", http_client=mocker.MagicMock())
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
    client = AsyncBaseClient(url="base_url", http_client=mocker.MagicMock())
    response = httpx.Response(status_code=200, content=json.dumps(response_content))

    with pytest.raises(GraphQLClientInvalidResponseError) as exc:
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
    client = AsyncBaseClient(url="base_url", http_client=mocker.MagicMock())

    with pytest.raises(GraphQLClientGraphQLMultiError):
        client.get_data(
            httpx.Response(status_code=200, content=json.dumps(response_content))
        )


@pytest.mark.parametrize(
    "response_content",
    [{"errors": [], "data": {}}, {"errors": None, "data": {}}, {"data": {}}],
)
def test_get_data_doesnt_raise_exception(mocker, response_content):
    client = AsyncBaseClient(url="base_url", http_client=mocker.MagicMock())

    data = client.get_data(
        httpx.Response(status_code=200, content=json.dumps(response_content))
    )

    assert data == response_content["data"]


@pytest.mark.asyncio
async def test_base_client_used_as_context_manager_closes_http_client(mocker):
    fake_client = mocker.AsyncMock()
    async with AsyncBaseClient(url="base_url", http_client=fake_client) as base_client:
        await base_client.execute("")

    assert fake_client.aclose.called
