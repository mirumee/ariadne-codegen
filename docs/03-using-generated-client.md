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

### Passing headers to client

Client (with default base client), takes passed headers and attaches them to every sent request.

```py
client = Client("https://example.com/graphql", {"Authorization": "Bearer token"})
```

### Using custom http client

The default base class http client can be replaced with another client:

```py
client = Client(http_client=CustomComplexHttpClient())
```

`CustomComplexHttpClient` needs to fulfill the following protocol for async client:

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

Protocol for sync client:

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

The protocol for sync client is also fulfilled by some commonly known classes, like `requests.Session`.
