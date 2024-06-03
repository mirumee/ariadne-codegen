from typing import Optional, Union

from . import (
    AppGraphQLField,
    PageInfoGraphQLField,
    ProductCountableConnectionGraphQLField,
    ProductCountableEdgeGraphQLField,
    ProductGraphQLField,
    ProductTypeCountableConnectionGraphQLField,
)
from .base_operation import GraphQLField


class PageInfoFields(GraphQLField):
    has_next_page: PageInfoGraphQLField = PageInfoGraphQLField("hasNextPage")
    has_previous_page: PageInfoGraphQLField = PageInfoGraphQLField("hasPreviousPage")
    start_cursor: PageInfoGraphQLField = PageInfoGraphQLField("startCursor")
    end_cursor: PageInfoGraphQLField = PageInfoGraphQLField("endCursor")

    def fields(self, *subfields: PageInfoGraphQLField) -> "PageInfoFields":
        self._subfields.extend(subfields)
        return self

    def __get__(self, instance, owner) -> "PageInfoFields":
        return PageInfoFields(name=self._name)


class AppFields(GraphQLField):
    id: AppGraphQLField = AppGraphQLField("id")

    def fields(self, *subfields: AppGraphQLField) -> "AppFields":
        self._subfields.extend(subfields)
        return self

    def __get__(self, instance, owner) -> "AppFields":
        return AppFields(name=self._name)


class ProductTypeCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    def fields(
        self,
        *subfields: Union[ProductTypeCountableConnectionGraphQLField, "PageInfoFields"]
    ) -> "ProductTypeCountableConnectionFields":
        self._subfields.extend(subfields)
        return self

    def __get__(self, instance, owner) -> "ProductTypeCountableConnectionFields":
        return ProductTypeCountableConnectionFields(name=self._name)


class ProductCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "ProductFields":
        return ProductFields("node")

    cursor: ProductCountableEdgeGraphQLField = ProductCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[ProductCountableEdgeGraphQLField, "ProductFields"]
    ) -> "ProductCountableEdgeFields":
        self._subfields.extend(subfields)
        return self

    def __get__(self, instance, owner) -> "ProductCountableEdgeFields":
        return ProductCountableEdgeFields(name=self._name)


class ProductCountableConnectionFields(GraphQLField):
    @classmethod
    def edges(cls) -> "ProductCountableEdgeFields":
        return ProductCountableEdgeFields("edges")

    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    total_count: ProductCountableConnectionGraphQLField = (
        ProductCountableConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            ProductCountableConnectionGraphQLField,
            "PageInfoFields",
            "ProductCountableEdgeFields",
        ]
    ) -> "ProductCountableConnectionFields":
        self._subfields.extend(subfields)
        return self

    def __get__(self, instance, owner) -> "ProductCountableConnectionFields":
        return ProductCountableConnectionFields(name=self._name)


class ProductFields(GraphQLField):
    id: ProductGraphQLField = ProductGraphQLField("id")
    slug: ProductGraphQLField = ProductGraphQLField("slug")
    name: ProductGraphQLField = ProductGraphQLField("name")

    def fields(self, *subfields: ProductGraphQLField) -> "ProductFields":
        self._subfields.extend(subfields)
        return self

    def __get__(self, instance, owner) -> "ProductFields":
        return ProductFields(name=self._name)
