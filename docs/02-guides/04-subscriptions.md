---
title: Subscriptions
---

# Subscriptions

To handle subscriptions, the default `AsyncBaseClient` uses
[websockets](https://github.com/python-websockets/websockets) and implements the
[graphql-transport-ws](https://github.com/enisdenjo/graphql-ws/blob/master/PROTOCOL.md)
subprotocol.

## Installation

Subscription support requires the `websockets` package, which is installed with the
`subscriptions` extra:

```
pip install ariadne-codegen[subscriptions]
```

Subscriptions are only available on the async client. The synchronous base client
(`async_client = false`) has no subscription support - see
[Async vs sync client](./10-async-vs-sync.md).

## Connecting

The WebSocket endpoint is separate from the HTTP `url` and is configured with
`ws_url`. Set it when constructing the client (the HTTP `url` is still used for
queries and mutations):

```py
from graphql_client.client import Client

client = Client(
    url="https://example.com/graphql",
    ws_url="wss://example.com/graphql",
)
```

## Consuming a subscription

Generated subscription methods return an `AsyncIterator` of the result model and
yield a new value for every message the server pushes, so iterate over them with
`async for`:

```py
async for result in client.get_users_counter():
    print(result.users_counter)
```

Here `get_users_counter` is the method generated from your `subscription` operation
(`subscription GetUsersCounter { usersCounter }`) and `result` is the typed response
model for that operation.

## Full example

Given a schema with a subscription field:

```graphql
type Subscription {
  usersCounter: Int!
}
```

and a subscription operation in your queries file:

```graphql
subscription GetUsersCounter {
  usersCounter
}
```

`ariadne-codegen` generates a `get_users_counter` method. Connect over WebSockets and
consume the stream with `async for`:

```py
import asyncio
from graphql_client.client import Client


async def main():
    client = Client(
        url="https://example.com/graphql",
        ws_url="wss://example.com/graphql",
    )
    async for result in client.get_users_counter():
        print("users online:", result.users_counter)


asyncio.run(main())
```

Each server push yields a new `GetUsersCounter` instance; the loop runs until the
server closes the subscription (or you `break` out of it).

## Connection arguments

Arguments `ws_origin` and `ws_headers` are added as headers to the handshake
request, and `ws_connection_init_payload` is used as the payload of the
[ConnectionInit](https://github.com/enisdenjo/graphql-ws/blob/master/PROTOCOL.md#connectioninit)
message. See [Using generated client](./03-using-generated-client.md#client-configuration)
for the full list of constructor arguments.
