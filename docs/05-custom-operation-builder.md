---
title: Custom operation builder
---

# Custom operation builder

The custom operation builder allows you to create complex GraphQL queries in a structured and intuitive way.

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

## Example pyproject.toml configuration.

`Note: queries_path is optional when enable_custom_operations is set to true`

```toml
[tool.ariadne-codegen]
schema_path = "schema.graphql"
include_comments = "none"
target_package_name = "example_client"
enable_custom_operations = true
```
