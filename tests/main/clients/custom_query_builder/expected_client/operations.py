__all__ = ["LIST_ALL_PRODUCTS_GQL"]

LIST_ALL_PRODUCTS_GQL = """
query ListAllProducts {
  products {
    edges {
      node {
        id
        slug
      }
    }
  }
}
"""
