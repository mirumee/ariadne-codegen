import importlib
import sys
from collections.abc import Iterator

import pytest

from ariadne_codegen.client_generators.dependencies import (
    async_base_client,
    async_base_client_no_upload,
    async_base_client_open_telemetry,
    async_base_client_open_telemetry_no_upload,
)


@pytest.fixture(
    params=[
        (async_base_client, "AsyncBaseClient"),
        (async_base_client_no_upload, "AsyncBaseClient"),
        (async_base_client_open_telemetry, "AsyncBaseClientOpenTelemetry"),
        (async_base_client_open_telemetry_no_upload, "AsyncBaseClientOpenTelemetry"),
    ],
    ids=lambda param: param[0].__name__.rsplit(".", maxsplit=1)[-1],
)
def client_class_without_websockets(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> Iterator[type]:
    module, class_name = request.param
    # None in sys.modules makes the import raise ImportError
    monkeypatch.setitem(sys.modules, name="websockets", value=None)
    monkeypatch.setitem(sys.modules, name="websockets.typing", value=None)
    try:
        yield getattr(importlib.reload(module), class_name)
    finally:
        monkeypatch.undo()
        # reload again so later tests get the real websockets imports back
        importlib.reload(module)


def test_init_accepts_ws_origin_without_websockets(
    client_class_without_websockets: type,
) -> None:
    client = client_class_without_websockets(ws_origin="test_origin")

    assert client.ws_origin == "test_origin"
