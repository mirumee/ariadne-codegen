---
title: Fragments and forward references
---

# Fragments and forward references

When an operation spreads a fragment, the generated result class subclasses the fragment class:

```python
# get_products.py
from .fragments import (
    ProductListItem,
    ProductListItemThumbnail,  # noqa: F401
)

class GetProductsProductsEdgesNode(ProductListItem):
    pass
```

Pydantic resolves the annotations a subclass inherits against the subclass's own module, so any class the fragment refers to by forward reference has to be importable there. That is what the second import is for. It carries `# noqa: F401` because the name only appears inside an inherited annotation, and your linter would otherwise call it unused.

This import is emitted for every generated client, regardless of the settings.
