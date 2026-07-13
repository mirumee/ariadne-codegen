---
title: Introduction
slug: /
---

# Ariadne Code Generator

[![Ariadne](https://ariadnegraphql.org/img/logo-horizontal-sm.png)](https://ariadnegraphql.org)

[![Build Status](https://github.com/mirumee/ariadne-codegen/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/mirumee/ariadne-codegen/actions)

Python code generator that turns a GraphQL schema and your operations into a fully typed, async (or sync) Python client built on Pydantic. You write your queries, mutations and subscriptions in GraphQL, and ariadne-codegen generates a typed Python method for each one, returning Pydantic models - so you get autocompletion and static type checking instead of hand-writing query strings and parsing raw JSON.

📖 **[Documentation](./01-introduction.md)** · [Step-by-step example](./02-guides/01-step-by-step-example.md) · [Configuration reference](./03-reference/01-configuration.md)

## Features

- **Fully typed models** - Pydantic models for schema types, inputs, enums, fragments, and every operation's result.
- **Typed client methods** - each query, mutation, and subscription becomes a method with typed arguments and a typed return value.
- **[Async or sync](./02-guides/10-async-vs-sync.md)** - generate an async client (default) or a synchronous one.
- **[Subscriptions](./02-guides/04-subscriptions.md)** - real-time updates over WebSockets (`graphql-transport-ws`).
- **[File uploads](./02-guides/05-file-uploads.md)** - multipart requests via the GraphQL multipart request spec.
- **[Custom scalars](./02-guides/06-custom-scalars.md)** - map GraphQL scalars to your own Python types with `serialize`/`parse` hooks.
- **[Extensible output](./02-guides/07-extending-types.md)** - inject mixins into generated models, copy in your own files, or swap the [base client](./03-reference/02-generated-code-dependencies.md) (custom auth, or to drop the `httpx`/`websockets` deps).
- **[Flexible schema sources](./02-guides/02-schema-sources.md)** - a local file, installed Python packages, or remote introspection.
- **[Plugin system](./04-plugins/01-intro.md)** - customize generation through hooks, plus ready-made plugins (shorter results, extracted operation strings, forward refs, …).
- **More** - [programmatic query building](./02-guides/12-custom-operation-builder.md), [OpenTelemetry tracing](./02-guides/09-opentelemetry.md), [multiple clients per project](./02-guides/08-multiple-clients.md), and a [schema-copy mode](./02-guides/11-schema-generation.md).

## Installation

```
pip install ariadne-codegen
```

Add subscription (WebSocket) support with:

```
pip install ariadne-codegen[subscriptions]
```

## Quickstart

Generate a typed client from three files.

**1. Describe your schema** in `schema.graphql`:

```graphql
type Query {
  hello(name: String!): String!
}
```

**2. Write the operations you need** in `queries.graphql`:

```graphql
query Greet($name: String!) {
  hello(name: $name)
}
```

**3. Point `ariadne-codegen` at them** in `pyproject.toml`:

```toml
[tool.ariadne-codegen]
schema_path = "schema.graphql"
queries_path = "queries.graphql"
```

Then generate the client:

```
ariadne-codegen
```

This creates a Python package (named `graphql_client` by default) next to your
config, with the typed client and Pydantic models generated from your schema and
operations:

```
graphql_client/
    __init__.py
    async_base_client.py   # networking base client
    base_model.py
    client.py              # the typed Client, with a greet() method
    enums.py
    exceptions.py
    greet.py               # result model for the Greet operation
    input_types.py
```

You get one result module per operation plus shared modules for enums, input types,
fragments and scalars. Import the client and use it right away:

```python
import asyncio
from graphql_client import Client


async def main():
    async with Client(url="https://example.com/graphql") as client:
        result = await client.greet(name="World")
        print(result.hello)


asyncio.run(main())
```

`greet` is a typed method generated from your `Greet` operation, and `result` is a
validated Pydantic model. See the [step-by-step example](./02-guides/01-step-by-step-example.md)
for a walk-through of everything that gets generated.


## Contributing

Contributions are welcome! See [Contributing](./05-community/01-contributing.md) for how to report bugs, work on issues, and open pull requests.

Also make sure you follow [@AriadneGraphQL](https://twitter.com/AriadneGraphQL) on Twitter for latest updates, news and random musings!

# Crafted with ❤️ by [Mirumee Labs](http://mirumee.com) <ariadne@mirumee.com>
