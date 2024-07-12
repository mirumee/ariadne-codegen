from typing import Any, Dict, Optional

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
        arguments: Dict[str, Dict[str, Any]] = {
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
        arguments: Dict[str, Dict[str, Any]] = {}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AppFields(field_name="app", arguments=cleared_arguments)

    @classmethod
    def product_types(cls) -> ProductTypeCountableConnectionFields:
        arguments: Dict[str, Dict[str, Any]] = {}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ProductTypeCountableConnectionFields(
            field_name="productTypes", arguments=cleared_arguments
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
        arguments: Dict[str, Dict[str, Any]] = {
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
