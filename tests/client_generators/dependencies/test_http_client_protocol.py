import httpx

from ariadne_codegen.client_generators.dependencies import (
    async_base_client,
    async_base_client_no_upload,
    async_base_client_open_telemetry,
    async_base_client_open_telemetry_no_upload,
    base_client,
    base_client_no_upload,
    base_client_open_telemetry,
    base_client_open_telemetry_no_upload,
)

# Annotated assignments below are checked by ty during lint: httpx clients
# must structurally satisfy every HttpClient protocol shipped with the clients.


def test_httpx_client_satisfies_sync_http_client_protocols():
    http_client = httpx.Client()

    protocols: tuple[
        base_client.HttpClient,
        base_client_no_upload.HttpClient,
        base_client_open_telemetry.HttpClient,
        base_client_open_telemetry_no_upload.HttpClient,
    ] = (http_client, http_client, http_client, http_client)

    assert all(protocol is http_client for protocol in protocols)


def test_httpx_async_client_satisfies_async_http_client_protocols():
    http_client = httpx.AsyncClient()

    protocols: tuple[
        async_base_client.HttpClient,
        async_base_client_no_upload.HttpClient,
        async_base_client_open_telemetry.HttpClient,
        async_base_client_open_telemetry_no_upload.HttpClient,
    ] = (http_client, http_client, http_client, http_client)

    assert all(protocol is http_client for protocol in protocols)
