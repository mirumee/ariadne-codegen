---
title: Async vs sync client
---

# Async vs sync client

By default the generated client is asynchronous - every operation is available as an
`async` method and the client inherits from `AsyncBaseClient`.

To generate a synchronous client instead, set `async_client` to `false`:

```toml
[tool.ariadne-codegen]
async_client = false
```

## What changes

|                        | Async (default)                     | Sync (`async_client = false`)     |
| ---------------------- | ----------------------------------- | --------------------------------- |
| Base class             | `AsyncBaseClient`                   | `BaseClient`                      |
| Operation methods      | `async def` (must be `await`ed)     | plain `def`                       |
| Context manager        | `async with`                        | `with`                            |
| Custom `http_client`   | async client (default `httpx.AsyncClient`) | sync client (default `httpx.Client`) |
| Subscriptions          | supported                           | **not supported**                 |

The generated method bodies mirror this - the async client does
`response = await self.execute(...)`, the sync client does `response = self.execute(...)`:

```py
# async
async def list_all_users(self, **kwargs: Any) -> ListAllUsers:
    ...
    response = await self.execute(query=query, ...)
    data = self.get_data(response)
    return ListAllUsers.model_validate(data)
```

```py
# sync
def list_all_users(self, **kwargs: Any) -> ListAllUsers:
    ...
    response = self.execute(query=query, ...)
    data = self.get_data(response)
    return ListAllUsers.model_validate(data)
```

## Subscriptions require the async client

Subscriptions are only available on the async client. If your operations include a
`subscription` while `async_client = false`, generation fails with:

```
Subscriptions are only available when using async client.
```

See [Subscriptions](./04-subscriptions.md).
