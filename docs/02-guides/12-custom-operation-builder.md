---
title: Custom operation builder
---

# Custom operation builder

The custom operation builder allows you to create complex GraphQL queries in a structured and intuitive way.

## Enabling

Set `enable_custom_operations = true` in your config. This mode generates additional
helper modules instead of (or alongside) the per-operation client methods, so
`queries_path` becomes optional:

```toml
[tool.ariadne-codegen]
schema_path = "schema.graphql"
enable_custom_operations = true
```

With it enabled, the following modules are generated in your package:

- `custom_fields.py` - a `…Fields` class per object type, used to select fields.
- `custom_typing_fields.py` - supporting types for field selection.
- `custom_queries.py` - a `Query` class with a builder method per root query field (generated only if the schema has a `Query` type).
- `custom_mutations.py` - a `Mutation` class with a builder method per root mutation field (generated only if the schema has a `Mutation` type).

The client also gains `query(...)`, `mutation(...)` and `execute_custom_operation(...)`
methods for executing the built operations.

## Example Code

```python
import asyncio
from graphql_client import Client
from graphql_client.custom_fields import (
    ProductFields,
    ProductTranslatableContentFields,
    ProductTranslationFields,
    TranslatableItemConnectionFields,
    TranslatableItemEdgeFields,
)
from graphql_client.custom_queries import Query
from graphql_client.enums import LanguageCodeEnum, TranslatableKinds


async def get_products():
    # Create a client instance with the specified URL and headers
    client = Client(
        url="https://saleor.cloud/graphql/",
        headers={"authorization": "bearer ..."},
    )

    # Build the queries
    product_query = Query.product(id="...", channel="channel-uk").fields(
        ProductFields.id,
        ProductFields.name,
    )

    translation_query = Query.translations(kind=TranslatableKinds.PRODUCT, first=10).fields(
        TranslatableItemConnectionFields.edges().alias("aliased_edges").fields(
            TranslatableItemEdgeFields.node.on(
                "ProductTranslatableContent",
                ProductTranslatableContentFields.id,
                ProductTranslatableContentFields.product_id,
                ProductTranslatableContentFields.name,
            )
        )
    )

    # Execute the queries with an operation name
    response = await client.query(
        product_query,
        translation_query,
        operation_name="get_products",
    )

    print(response)

# Run the async function
asyncio.run(get_products())
```

## Explanation

1. Building the Product Query:
   1. The Query.product(id="...", channel="channel-uk") initiates a query for a product with the specified ID and channel.
   2. .fields(ProductFields.id, ProductFields.name) specifies the fields to retrieve for the product: id and name.
2. Building the Translation Query:
   1. The Query.translations(kind=TranslatableKinds.PRODUCT, first=10) initiates a query for product translations.
   2. .fields(...) specifies the fields to retrieve for the translations.
   3. .alias("aliased_edges") renames the edges field to aliased_edges.
   4. .on("ProductTranslatableContent", ...) specifies the fields to retrieve if the node is of type ProductTranslatableContent: id, product_id, and name.
3. Executing the Queries:
   1. The client.query(...) method is called with the built queries and an operation name "get_products".
   2. This method sends the queries to the server and retrieves the response.

Unlike the per-operation client methods, `client.query(...)` and
`client.mutation(...)` return the raw response as a `dict[str, Any]` - the result is
not parsed into a generated Pydantic model.

## Building mutations

Mutations are built the same way, using the generated `Mutation` class from
`custom_mutations` and executed with `client.mutation(...)`:

```python
from graphql_client import Client
from graphql_client.custom_fields import ProductFields
from graphql_client.custom_mutations import Mutation


async def update_product():
    client = Client(url="https://saleor.cloud/graphql/")

    build = Mutation.product_update(id="...").fields(
        ProductFields.id,
        ProductFields.name,
    )
    response = await client.mutation(build, operation_name="update_product")
    print(response)
```

## Example pyproject.toml configuration.

`Note: queries_path is optional when enable_custom_operations is set to true`

```toml
[tool.ariadne-codegen]
schema_path = "schema.graphql"
include_comments = "none"
target_package_name = "example_client"
enable_custom_operations = true
```
