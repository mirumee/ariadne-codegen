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
            field_name="products", channel=channel, first=first
        )

    @classmethod
    def app(cls) -> AppFields:
        return AppFields(field_name="app")

    @classmethod
    def product_types(cls) -> ProductTypeCountableConnectionFields:
        return ProductTypeCountableConnectionFields(field_name="productTypes")

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
            before=before,
            after=after,
            first=first,
            last=last,
        )
