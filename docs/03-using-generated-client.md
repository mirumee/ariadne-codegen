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

For more complex scenarios, you can pass your own http client:

```py
client = Client(http_client=CustomComplexHttpClient())
```

`CustomComplexHttpClient` needs to be an instance of `httpx.AsyncClient` for async client, or `httpx.Client` for sync.
