import json
from datetime import datetime
from typing import Any, Optional
from unittest.mock import ANY

import httpx
import pytest

from ariadne_codegen.client_generators.dependencies.base_client import BaseClient
from ariadne_codegen.client_generators.dependencies.base_model import UNSET, BaseModel
from ariadne_codegen.client_generators.dependencies.exceptions import (
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQlClientInvalidResponseError,
)

from ...utils import decode_multipart_request


def test_execute_sends_post_to_correct_url_with_correct_payload(httpx_mock):
    httpx_mock.add_response()
    client = BaseClient(url="http://base_url/endpoint")
    query_str = """
    query Abc($v: String!) {
        abc(v: $v) {
            field1
        }
    }
    """

    client.execute(query_str, {"v": "Xyz"})

    request = httpx_mock.get_request()
    assert request.url == "http://base_url/endpoint"
    content = json.loads(request.content)
    assert content == {"query": query_str, "variables": {"v": "Xyz"}}


def test_execute_parses_pydantic_variables_before_sending(httpx_mock):
    class TestModel1(BaseModel):
        a: int

    class TestModel2(BaseModel):
        nested: TestModel1

    httpx_mock.add_response()
    client = BaseClient(url="http://base_url")
    query_str = """
    query Abc($v1: TestModel1!, $v2: TestModel2) {
        abc(v1: $v1, v2: $v2){
            field1
        }
    }
    """

    client.execute(
        query_str, {"v1": TestModel1(a=5), "v2": TestModel2(nested=TestModel1(a=10))}
    )

    request = httpx_mock.get_request()
    content = json.loads(request.content)
    assert content == {
        "query": query_str,
        "variables": {"v1": {"a": 5}, "v2": {"nested": {"a": 10}}},
    }


def test_execute_correctly_parses_top_level_list_variables(httpx_mock):
    class TestModel1(BaseModel):
        a: int

    httpx_mock.add_response()
    client = BaseClient(url="http://base_url")
    query_str = """
    query Abc($v1: [[TestModel1!]!]!) {
        abc(v1: $v1){
            field1
        }
    }
    """

    client.execute(
        query_str,
        {
            "v1": [[TestModel1(a=1), TestModel1(a=2)]],
        },
    )

    request = httpx_mock.get_request()
    content = json.loads(request.content)
    assert content == {
        "query": query_str,
        "variables": {"v1": [[{"a": 1}, {"a": 2}]]},
    }
    assert not any(isinstance(x, BaseModel) for x in content["variables"]["v1"][0])


def test_execute_sends_payload_without_unset_arguments(httpx_mock):
    httpx_mock.add_response()
    client = BaseClient(url="http://base_url")
    query_str = """
    query Abc($arg1: TestInputA, $arg2: String, $arg3: Float, $arg4: Int!) {
        abc(arg1: $arg1, arg2: $arg2, arg3: $arg3, arg4: $arg4){
            field1
        }
    }
    """

    client.execute(query_str, {"arg1": UNSET, "arg2": UNSET, "arg3": None, "arg4": 2})

    request = httpx_mock.get_request()
    content = json.loads(request.content)
    assert content == {
        "query": query_str,
        "variables": {"arg3": None, "arg4": 2},
    }


def test_execute_sends_payload_without_unset_input_fields(httpx_mock):
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
    client = BaseClient(url="http://base_url")
    query_str = """
    query Abc($arg: TestInputB) {
        abc(arg: $arg){
            field1
        }
    }
    """

    client.execute(
        query_str,
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
        "variables": {
            "arg": {
                "required_a": "a",
                "input_b1": {"required_b": "b"},
                "input_b3": None,
            }
        },
    }


def test_execute_sends_payload_with_serialized_datetime_without_exception(httpx_mock):
    httpx_mock.add_response()
    client = BaseClient(url="http://base_url")
    query_str = "query Abc($arg: DATETIME) { abc }"
    arg_value = datetime(2023, 12, 31, 10, 15)

    client.execute(query_str, {"arg": arg_value})

    request = httpx_mock.get_request()
    content = json.loads(request.content)
    assert content["variables"]["arg"] == arg_value.isoformat()


def test_execute_sends_request_with_correct_content_type(httpx_mock):
    httpx_mock.add_response()
    client = BaseClient(url="http://base_url")

    client.execute("query Abc { abc }", {})

    request = httpx_mock.get_request()
    assert request.headers["Content-Type"] == "application/json"


def test_execute_sends_request_with_extra_headers_and_correct_content_type(httpx_mock):
    httpx_mock.add_response()
    client = BaseClient(url="http://base_url", headers={"h_key": "h_value"})

    client.execute("query Abc { abc }", {})

    request = httpx_mock.get_request()
    assert request.headers["h_key"] == "h_value"
    assert request.headers["Content-Type"] == "application/json"


def test_execute_sends_file_with_multipart_form_data_content_type(httpx_mock, txt_file):
    httpx_mock.add_response()

    client = BaseClient(url="http://base_url")
    client.execute("query Abc($file: Upload!) { abc(file: $file) }", {"file": txt_file})

    request = httpx_mock.get_request()
    assert "multipart/form-data" in request.headers["Content-Type"]


def test_execute_sends_file_as_multipart_request(httpx_mock, txt_file):
    httpx_mock.add_response()
    query_str = "query Abc($file: Upload!) { abc(file: $file) }"

    client = BaseClient(url="http://base_url")
    client.execute(query_str, {"file": txt_file})

    request = httpx_mock.get_request()
    request.read()
    assert "multipart/form-data" in request.headers["Content-Type"]
    sent_parts = decode_multipart_request(request)

    assert sent_parts["operations"]
    decoded_operations = json.loads(sent_parts["operations"].content)
    assert decoded_operations == {"query": query_str, "variables": {"file": None}}

    assert sent_parts["map"]
    decoded_map = json.loads(sent_parts["map"].content)
    assert decoded_map == {"0": ["variables.file"]}

    assert sent_parts["0"]
    assert sent_parts["0"].headers[b"Content-Type"] == b"text/plain"
    assert b"txt_file.txt" in sent_parts["0"].headers[b"Content-Disposition"]
    assert sent_parts["0"].content == b"abcdefgh"


def test_execute_sends_file_from_memory(httpx_mock, in_memory_txt_file):
    httpx_mock.add_response()
    query_str = "query Abc($file: Upload!) { abc(file: $file) }"

    client = BaseClient(url="http://base_url")
    client.execute(query_str, {"file": in_memory_txt_file})

    request = httpx_mock.get_request()
    request.read()
    assert "multipart/form-data" in request.headers["Content-Type"]
    sent_parts = decode_multipart_request(request)

    assert sent_parts["operations"]
    decoded_operations = json.loads(sent_parts["operations"].content)
    assert decoded_operations == {"query": query_str, "variables": {"file": None}}

    assert sent_parts["map"]
    decoded_map = json.loads(sent_parts["map"].content)
    assert decoded_map == {"0": ["variables.file"]}

    assert sent_parts["0"]
    assert sent_parts["0"].headers[b"Content-Type"] == b"text/plain"
    assert b"in_memory.txt" in sent_parts["0"].headers[b"Content-Disposition"]
    assert sent_parts["0"].content == b"123456"


def test_execute_sends_multiple_files(httpx_mock, txt_file, png_file):
    httpx_mock.add_response()
    query_str = "query Abc($files: [Upload!]!) { abc(files: $files) }"

    client = BaseClient(url="http://base_url")
    client.execute(query_str, {"files": [txt_file, png_file]})

    request = httpx_mock.get_request()
    request.read()
    assert "multipart/form-data" in request.headers["Content-Type"]
    sent_parts = decode_multipart_request(request)

    assert sent_parts["operations"]
    decoded_operations = json.loads(sent_parts["operations"].content)
    assert decoded_operations == {
        "query": query_str,
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


def test_execute_sends_nested_file(httpx_mock, txt_file):
    class InputType(BaseModel):
        file_: Any

    httpx_mock.add_response()
    query_str = "query Abc($input: InputType!) { abc(input: $input) }"

    client = BaseClient(url="http://base_url")
    client.execute(query_str, {"input": InputType(file_=txt_file)})

    request = httpx_mock.get_request()
    request.read()
    assert "multipart/form-data" in request.headers["Content-Type"]
    sent_parts = decode_multipart_request(request)

    assert sent_parts["operations"]
    decoded_operations = json.loads(sent_parts["operations"].content)
    assert decoded_operations == {
        "query": query_str,
        "variables": {"input": {"file_": None}},
    }

    assert sent_parts["map"]
    decoded_map = json.loads(sent_parts["map"].content)
    assert decoded_map == {"0": ["variables.input.file_"]}

    assert sent_parts["0"]
    assert sent_parts["0"].headers[b"Content-Type"] == b"text/plain"
    assert b"txt_file.txt" in sent_parts["0"].headers[b"Content-Disposition"]
    assert sent_parts["0"].content == b"abcdefgh"


def test_execute_sends_each_file_only_once(httpx_mock, txt_file):
    httpx_mock.add_response()
    query_str = "query Abc($files: [Upload!]!) { abc(files: $files) }"

    client = BaseClient(url="http://base_url")
    client.execute(query_str, {"files": [txt_file, txt_file]})

    request = httpx_mock.get_request()
    request.read()
    assert "multipart/form-data" in request.headers["Content-Type"]
    sent_parts = decode_multipart_request(request)

    assert sent_parts["operations"]
    decoded_operations = json.loads(sent_parts["operations"].content)
    assert decoded_operations == {
        "query": query_str,
        "variables": {"files": [None, None]},
    }

    assert sent_parts["map"]
    decoded_map = json.loads(sent_parts["map"].content)
    assert decoded_map == {"0": ["variables.files.0", "variables.files.1"]}

    assert sent_parts["0"]
    assert sent_parts["0"].headers[b"Content-Type"] == b"text/plain"
    assert b"txt_file.txt" in sent_parts["0"].headers[b"Content-Disposition"]
    assert sent_parts["0"].content == b"abcdefgh"


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
    client = BaseClient(url="base_url", http_client=mocker.MagicMock())
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
    client = BaseClient(url="base_url", http_client=mocker.MagicMock())
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
    client = BaseClient(url="base_url", http_client=mocker.MagicMock())

    with pytest.raises(GraphQLClientGraphQLMultiError):
        client.get_data(
            httpx.Response(status_code=200, content=json.dumps(response_content))
        )


@pytest.mark.parametrize(
    "response_content",
    [{"errors": [], "data": {}}, {"errors": None, "data": {}}, {"data": {}}],
)
def test_get_data_doesnt_raise_exception(mocker, response_content):
    client = BaseClient(url="base_url", http_client=mocker.MagicMock())

    data = client.get_data(
        httpx.Response(status_code=200, content=json.dumps(response_content))
    )

    assert data == response_content["data"]


def test_base_client_used_as_context_manager_closes_http_client(mocker):
    fake_client = mocker.MagicMock()
    with BaseClient(url="base_url", http_client=fake_client) as base_client:
        base_client.execute("")

    assert fake_client.close.called


@pytest.fixture
def mocker_get_tracer(mocker):
    return mocker.patch(
        "ariadne_codegen.client_generators.dependencies.base_client.get_tracer"
    )


@pytest.fixture
def mocked_start_as_current_span(mocker_get_tracer):
    return mocker_get_tracer.return_value.start_as_current_span


def test_base_client_with_given_tracker_str_uses_global_tracker(mocker_get_tracer):
    BaseClient(url="http://base_url", tracer="tracker name")

    assert mocker_get_tracer.call_count == 1


def test_execute_creates_root_span(httpx_mock, mocked_start_as_current_span):
    httpx_mock.add_response()
    client = BaseClient(url="http://base_url", tracer="tracker")

    client.execute("query GetHello { hello }")

    mocked_start_as_current_span.assert_any_call("GraphQL Operation", context=ANY)
    with mocked_start_as_current_span.return_value as span:
        span.set_attribute.assert_any_call("component", "GraphQL Client")


def test_execute_creates_root_span_with_custom_name(
    httpx_mock, mocked_start_as_current_span
):
    httpx_mock.add_response()
    client = BaseClient(
        url="http://base_url", tracer="tracker", root_span_name="root_span"
    )

    client.execute("query GetHello { hello }")

    mocked_start_as_current_span.assert_any_call("root_span", context=ANY)


def test_execute_creates_root_span_with_custom_context(
    httpx_mock, mocked_start_as_current_span
):
    httpx_mock.add_response()
    client = BaseClient(
        url="http://base_url", tracer="tracker", root_context={"abc": 123}
    )

    client.execute("query GetHello { hello }")

    mocked_start_as_current_span.assert_any_call(
        "GraphQL Operation", context={"abc": 123}
    )


def test_execute_creates_span_for_json_http_request(
    httpx_mock, mocked_start_as_current_span
):
    httpx_mock.add_response()
    client = BaseClient(url="http://base_url", tracer="tracker")

    client.execute("query GetHello { hello }", variables={"a": 1, "b": {"bb": 2}})

    mocked_start_as_current_span.assert_any_call("json request", context=ANY)
    with mocked_start_as_current_span.return_value as span:
        span.set_attribute.assert_any_call("component", "GraphQL Client")
        span.set_attribute.assert_any_call("query", "query GetHello { hello }")
        span.set_attribute.assert_any_call(
            "variables", json.dumps({"a": 1, "b": {"bb": 2}})
        )


def test_execute_creates_span_for_multipart_request(
    httpx_mock, txt_file, mocked_start_as_current_span
):
    httpx_mock.add_response()
    client = BaseClient(url="http://base_url", tracer="tracker")

    client.execute(
        "query Abc($file: Upload!) { abc(file: $file) }",
        {"file": txt_file, "a": 1.0, "b": {"bb": 2}},
    )

    mocked_start_as_current_span.assert_any_call("multipart request", context=ANY)
    with mocked_start_as_current_span.return_value as span:
        span.set_attribute.assert_any_call("component", "GraphQL Client")
        span.set_attribute.assert_any_call(
            "query", "query Abc($file: Upload!) { abc(file: $file) }"
        )
        span.set_attribute.assert_any_call(
            "variables", json.dumps({"file": None, "a": 1.0, "b": {"bb": 2}})
        )
        span.set_attribute.assert_any_call("map", json.dumps({"0": ["variables.file"]}))
