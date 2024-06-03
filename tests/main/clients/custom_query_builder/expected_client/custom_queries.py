from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from .base_operation import BaseGraphQLOperation

if TYPE_CHECKING:
    from .custom_fields import (
        AppGraphQLField,
        PageInfoFields,
        ProductCountableConnectionGraphQLField,
        ProductCountableEdgeFields,
    )


class ProductsGraphQLQuery(BaseGraphQLOperation):
    def fields(
        self,
        *args: Union[
            "ProductCountableEdgeFields",
            "PageInfoFields",
            "ProductCountableConnectionGraphQLField",
        ]
    ) -> "ProductsGraphQLQuery":
        self._fields.extend(args)
        return self


class AppGraphQLQuery(BaseGraphQLOperation):
    def fields(self, *args: "AppGraphQLField") -> "AppGraphQLQuery":
        self._fields.extend(args)
        return self


class ProductTypesGraphQLQuery(BaseGraphQLOperation):
    def fields(self, *args: "PageInfoFields") -> "ProductTypesGraphQLQuery":
        self._fields.extend(args)
        return self


def clean_arguments(**kwargs: Any) -> Dict[str, Any]:
    return {key: value for key, value in kwargs.items() if value is not None}


class Query:
    @classmethod
    def products(
        cls, *, channel: Optional[str] = None, first: Optional[int] = None
    ) -> ProductsGraphQLQuery:
        return ProductsGraphQLQuery(
            name="products", arguments=clean_arguments(channel=channel, first=first)
        )

    @classmethod
    def app(cls) -> AppGraphQLQuery:
        return AppGraphQLQuery(name="app", arguments=clean_arguments())

    @classmethod
    def product_types(cls) -> ProductTypesGraphQLQuery:
        return ProductTypesGraphQLQuery(
            name="productTypes", arguments=clean_arguments()
        )
