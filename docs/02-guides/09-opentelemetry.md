---
title: Open Telemetry
---

# Open Telemetry

When the config option `opentelemetry_client` is set to `true` then the default,
included base client is replaced with one that implements opt-in Open Telemetry
support. By default this support does nothing, but when the `opentelemetry-api`
package is installed and the `tracer` argument is provided then the client will
create spans with data about performed requests.

## Enabling

Turn it on in your config:

```toml
[tool.ariadne-codegen]
opentelemetry_client = true
```

The exact base client that gets generated depends on this option together with
`async_client` and `multipart_uploads` - you get an async or sync variant, with or
without multipart upload support. Regardless of the variant, the tracing arguments
below work the same way.

The `opentelemetry` import is optional: if the package is not installed the tracing
code is a no-op, so the generated client still works - it just doesn't produce spans.
To actually export spans, install and configure OpenTelemetry (`opentelemetry-api`
plus an SDK/exporter).

## Usage

Pass a `tracer` (an OpenTelemetry `Tracer`, or a string name that is resolved via
`get_tracer`) when constructing the client:

```py
from opentelemetry import trace
from graphql_client.client import Client

# A configured TracerProvider/exporter is assumed to be set up elsewhere.
tracer = trace.get_tracer("my-app")

client = Client(
    url="https://example.com/graphql",
    tracer=tracer,                     # or tracer="my-app"
    root_span_name="MyGraphQLCall",
)
```

## Tracing arguments

Tracing arguments handled by `BaseClientOpenTelemetry`:

- `tracer`: `Optional[Union[str, Tracer]] = None` - tracer object or name which will be passed to the `get_tracer` method
- `root_context`: `Optional[Context] = None` - optional context added to root span
- `root_span_name` - name of root span; defaults to `"GraphQL Operation"`

`AsyncBaseClientOpenTelemetry` supports all arguments which `BaseClientOpenTelemetry`
does, but also exposes additional arguments regarding websockets:

- `ws_root_context`: `Optional[Context] = None` - optional context added to root span for websocket connection
- `ws_root_span_name`: `str = "GraphQL Subscription"` - name of root span for websocket connection
