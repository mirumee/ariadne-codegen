import importlib
import os
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner
from httpx import ASGITransport, AsyncClient

from ariadne_codegen.main import main

from .generated_client.api import app as api_app


@pytest.fixture(scope="module")
def generated_client(tmp_path_factory):
    old_cwd = Path.cwd()
    tmp_cwd = tmp_path_factory.mktemp("tmp_cwd")

    source_files_dir = Path(__file__).parent / "generated_client"
    for filename in [
        "custom_scalars.py",
        "pyproject.toml",
        "queries.graphql",
        "schema.graphql",
    ]:
        tmp_cwd.joinpath(filename).write_text(
            source_files_dir.joinpath(filename).read_text()
        )

    os.chdir(tmp_cwd)
    CliRunner().invoke(main)

    client_name = "generated_client"
    init_path = tmp_cwd / client_name / "__init__.py"

    spec = importlib.util.spec_from_file_location(client_name, init_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    yield module

    os.chdir(old_cwd)


@pytest.fixture
def http_client():
    transport = ASGITransport(app=api_app)
    return AsyncClient(base_url="http://127.0.0.1:8000", transport=transport)


@pytest.fixture
def Client(generated_client):  # pylint: disable=invalid-name
    return generated_client.Client


@pytest.fixture
def CustomScalar(generated_client):  # pylint: disable=invalid-name
    return generated_client.custom_scalars.CustomScalar


@pytest.fixture
def GetA(generated_client):  # pylint: disable=invalid-name
    return generated_client.GetA


@pytest.fixture
def GetB(generated_client):  # pylint: disable=invalid-name
    return generated_client.GetB


@pytest.fixture
def GetC(generated_client):  # pylint: disable=invalid-name
    return generated_client.GetC


@pytest.fixture
def CustomInput(generated_client):  # pylint: disable=invalid-name
    return generated_client.CustomInput


@pytest.fixture
def mocked_parse(generated_client):
    parse = generated_client.custom_scalars.mocked_parse
    parse.reset_mock()
    return parse


@pytest.fixture
def mocked_serialize(generated_client):
    serialize = generated_client.custom_scalars.mocked_serialize
    serialize.reset_mock()
    return serialize


@pytest.mark.asyncio
async def test_get_a_uses_parse(
    http_client, Client, CustomScalar, GetA, mocked_parse, mocked_serialize
):  # pylint: disable=invalid-name
    async with Client(url="/graphql/", http_client=http_client) as client:
        result = await client.get_a()

    assert isinstance(result, GetA)
    assert isinstance(result.query_a, CustomScalar)
    assert result.query_a.value == "AAA"
    assert mocked_parse.call_count == 1
    assert mocked_parse.call_args[0] == ("AAA",)
    assert not mocked_serialize.called


@pytest.mark.asyncio
async def test_get_b_uses_parse_for_result_and_serialize_for_input(
    http_client, Client, CustomScalar, GetB, mocked_parse, mocked_serialize
):  # pylint: disable=invalid-name
    custom_scalar = CustomScalar("test")
    async with Client(url="/graphql/", http_client=http_client) as client:
        result = await client.get_b(custom_scalar)

    assert isinstance(result, GetB)
    assert isinstance(result.query_b, CustomScalar)
    assert result.query_b.value == "testBBB"
    assert mocked_parse.call_count == 1
    assert mocked_parse.call_args[0] == ("testBBB",)
    assert mocked_serialize.call_count == 1
    assert mocked_serialize.call_args[0] == (custom_scalar,)


@pytest.mark.asyncio
async def test_get_c_uses_parse_for_result_and_serialize_for_input(
    Client, GetC, CustomInput, CustomScalar, http_client, mocked_parse, mocked_serialize
):  # pylint: disable=invalid-name
    custom_scalar = CustomScalar("abc")
    async with Client(url="/graphql/", http_client=http_client) as client:
        result = await client.get_c(CustomInput(value=custom_scalar))

    assert isinstance(result, GetC)
    assert isinstance(result.query_c, CustomScalar)
    assert result.query_c.value == "abcCCC"
    assert mocked_parse.call_count == 1
    assert mocked_parse.call_args[0] == ("abcCCC",)
    assert mocked_serialize.call_count == 1
    assert mocked_serialize.call_args[0] == (custom_scalar,)
