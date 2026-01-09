from typing import Any, Optional

from .custom_fields import (
    AppFields,
    ProductCountableConnectionFields,
    ProductTypeCountableConnectionFields,
    StoreFields,
    TranslatableItemConnectionFields,
)


class Query:
    @classmethod
    def products(
        cls, *, channel: Optional[str] = None, first: Optional[int] = None
    ) -> ProductCountableConnectionFields:
        arguments: dict[str, dict[str, Any]] = {
            "channel": {"type": "String", "value": channel},
            "first": {"type": "Int", "value": first},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ProductCountableConnectionFields(
            field_name="products", arguments=cleared_arguments
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
        arguments: dict[str, dict[str, Any]] = {
            "before": {"type": "String", "value": before},
            "after": {"type": "String", "value": after},
            "first": {"type": "Int", "value": first},
            "last": {"type": "Int", "value": last},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return TranslatableItemConnectionFields(
            field_name="translations", arguments=cleared_arguments
        )

    @classmethod
    def store(cls) -> StoreFields:
        return StoreFields(field_name="store")
