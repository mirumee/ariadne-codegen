from typing import Any, Optional

from .custom_fields import (
    AppFields,
    ProductCountableConnectionFields,
    ProductTypeCountableConnectionFields,
    TranslatableItemConnectionFields,
)


class Query:
    @classmethod
    def products(
        cls, *, channel: Optional[str] = None, first: Optional[int] = None
    ) -> ProductCountableConnectionFields:
        return ProductCountableConnectionFields(
            field_name="products",
            arguments={
                "channel": {"type": "String", "value": channel},
                "first": {"type": "Int", "value": first},
            },
        )

    @classmethod
    def app(cls) -> AppFields:
        return AppFields(field_name="app", arguments={})

    @classmethod
    def product_types(cls) -> ProductTypeCountableConnectionFields:
        return ProductTypeCountableConnectionFields(
            field_name="productTypes", arguments={}
        )

    @classmethod
    def translations(
        cls,
        *,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None
    ) -> TranslatableItemConnectionFields:
        return TranslatableItemConnectionFields(
            field_name="translations",
            arguments={
                "before": {"type": "String", "value": before},
                "after": {"type": "String", "value": after},
                "first": {"type": "Int", "value": first},
                "last": {"type": "Int", "value": last},
            },
        )
