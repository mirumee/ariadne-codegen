---
title: Using generated client
---

# Using generated client

Generated client can be imported from package:

```py
from {target_package_name}.{client_file_name} import {client_name}
```

Example with default settings:

```py
from graphql_client.client import Client
```

Initialize the imported client with the server URL:

```py
client = Client("https://example.com/graphql")
```

The client (with the default base client) takes passed headers and attaches them to every sent request.

```py
client = Client("https://example.com/graphql", {"Authorization": "Bearer token"})
```

For more complex scenarios, you can pass your own HTTP client - see [Advanced HTTP configuration with httpx clients](#advanced-http-configuration-with-httpx-clients) or [with a custom client](#advanced-http-configuration-with-a-custom-client).

## Using the client as a context manager

Both base clients support the context manager protocol, which closes the underlying
HTTP client on exit. Use `async with` for the async client:

```py
async with Client(url="https://example.com/graphql") as client:
    result = await client.list_all_users()
```

and `with` for the synchronous client:

```py
with Client(url="https://example.com/graphql") as client:
    result = client.list_all_users()
```

## Client configuration

The generated client inherits its constructor from the base client. With the default
async base client (`AsyncBaseClient`), all constructor arguments are optional:

```py
client = Client(
    url="https://example.com/graphql",
    headers={"Authorization": "Bearer token"},
    http_client=None,                 # supply your own HTTP client if needed
    ws_url="wss://example.com/graphql",
    ws_headers={"Authorization": "Bearer token"},
    ws_origin="https://example.com",
    ws_connection_init_payload={"Authorization": "Bearer token"},
)
```

- `url` (defaults to `""`) - HTTP endpoint the client sends operations to.
- `headers` (defaults to `None`) - headers attached to every HTTP request. When no `http_client` is supplied, they are also used to build the default `httpx` client.
- `http_client` (defaults to `None`) - your own HTTP client instance; when none is provided a default `httpx` client is used. See [Advanced HTTP configuration with httpx clients](#advanced-http-configuration-with-httpx-clients) and [with a custom client](#advanced-http-configuration-with-a-custom-client) for details.
- `ws_url` (defaults to `""`) - WebSocket endpoint used for subscriptions.
- `ws_headers` (defaults to `None`) - headers added to the WebSocket handshake request.
- `ws_origin` (defaults to `None`) - value of the `Origin` header for the WebSocket handshake.
- `ws_connection_init_payload` (defaults to `None`) - payload sent in the `ConnectionInit` message.

The `ws_*` arguments only exist on the async base client (subscriptions are not
supported by the synchronous client). See [Subscriptions](./04-subscriptions.md) for
details. The synchronous base client (`async_client = false`) accepts only `url`,
`headers` and `http_client` - see [Async vs sync client](./10-async-vs-sync.md).

If you enable the OpenTelemetry base client (`opentelemetry_client = true`), the
constructor also accepts tracing arguments - see [Open Telemetry](./09-opentelemetry.md).

## Advanced HTTP configuration with httpx clients

When you don't supply an `http_client`, the base client builds a default
[httpx](https://www.python-httpx.org/) client (`httpx.AsyncClient`/`httpx.Client`),
passing only `headers` to it; `url` is stored separately and used as the target of each
request. Any HTTP behaviour beyond that (authentication, timeouts, proxies, HTTP/2, SSL
verification, cookies, connection limits, custom transports/retries, event hooks,
etc.) is configured on the httpx client itself. Build a configured httpx client and
pass it as `http_client`:

```py
import httpx
from graphql_client.client import Client

http_client = httpx.AsyncClient(
    base_url="https://example.com/graphql",
    auth=("user", "pass"),
    timeout=httpx.Timeout(10.0),
    http2=True,
    verify=False,
    proxy="http://localhost:8080",
    limits=httpx.Limits(max_connections=100),
    headers={"Authorization": "Bearer token"},
)

client = Client(http_client=http_client)
```

When you pass your own `http_client`, the client sends every request through it as-is.
The `headers` you would otherwise pass to `Client` are *not* merged into requests (they
only build the default client), so set them directly on the httpx client. Configure the
endpoint either by passing `url` to `Client` or by setting `base_url` on the httpx client
(as above). Refer to the
[httpx `Client` / `AsyncClient` API](https://www.python-httpx.org/api/#client)
for the full list of options.

## Advanced HTTP configuration with a custom client

The default base class HTTP client can be replaced with any client - it doesn't have to
be httpx, it only needs to fulfill the expected protocol:

```py
client = Client(http_client=CustomComplexHttpClient())
```

`CustomComplexHttpClient` needs to fulfill the following protocol for the async client:

```py
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
```

Protocol for the sync client:

```py
class Response(Protocol):
    status_code: int

    def json(self, **kwargs: Any) -> Any: ...


class HttpClient(Protocol):
    def post(
        self,
        url: Any | str,
        json: Any | None = None,
        data: Any | None = None,
        files: Any | None = None,
        headers: Any | None = None,
        **kwargs: Any,
    ) -> Response: ...

    def close(self) -> None: ...
```

The protocol for the sync client is also fulfilled by some commonly known classes, like `requests.Session`.