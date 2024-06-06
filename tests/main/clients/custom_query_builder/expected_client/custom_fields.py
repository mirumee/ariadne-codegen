from typing import Optional, Union

from . import (
    AppGraphQLField,
    CollectionTranslatableContentGraphQLField,
    MetadataErrorGraphQLField,
    MetadataItemGraphQLField,
    ObjectWithMetadataInterface,
    PageInfoGraphQLField,
    ProductCountableConnectionGraphQLField,
    ProductCountableEdgeGraphQLField,
    ProductGraphQLField,
    ProductTranslatableContentGraphQLField,
    ProductTypeCountableConnectionGraphQLField,
    TranslatableItemConnectionGraphQLField,
    TranslatableItemEdgeGraphQLField,
    TranslatableItemUnion,
    UpdateMetadataGraphQLField,
)
from .base_operation import GraphQLField


class AppFields(GraphQLField):
    id: AppGraphQLField = AppGraphQLField("id")

    def fields(self, *subfields: AppGraphQLField) -> "AppFields":
        self._subfields.extend(subfields)
        return self


class CollectionTranslatableContentFields(GraphQLField):
    id: CollectionTranslatableContentGraphQLField = (
        CollectionTranslatableContentGraphQLField("id")
    )
    collection_id: CollectionTranslatableContentGraphQLField = (
        CollectionTranslatableContentGraphQLField("collectionId")
    )
    seo_title: CollectionTranslatableContentGraphQLField = (
        CollectionTranslatableContentGraphQLField("seoTitle")
    )
    seo_description: CollectionTranslatableContentGraphQLField = (
        CollectionTranslatableContentGraphQLField("seoDescription")
    )
    name: CollectionTranslatableContentGraphQLField = (
        CollectionTranslatableContentGraphQLField("name")
    )
    description: CollectionTranslatableContentGraphQLField = (
        CollectionTranslatableContentGraphQLField("description")
    )

    def fields(
        self, *subfields: CollectionTranslatableContentGraphQLField
    ) -> "CollectionTranslatableContentFields":
        self._subfields.extend(subfields)
        return self


class MetadataErrorFields(GraphQLField):
    field: MetadataErrorGraphQLField = MetadataErrorGraphQLField("field")
    message: MetadataErrorGraphQLField = MetadataErrorGraphQLField("message")
    code: MetadataErrorGraphQLField = MetadataErrorGraphQLField("code")

    def fields(self, *subfields: MetadataErrorGraphQLField) -> "MetadataErrorFields":
        self._subfields.extend(subfields)
        return self


class MetadataItemFields(GraphQLField):
    key: MetadataItemGraphQLField = MetadataItemGraphQLField("key")
    value: MetadataItemGraphQLField = MetadataItemGraphQLField("value")

    def fields(self, *subfields: MetadataItemGraphQLField) -> "MetadataItemFields":
        self._subfields.extend(subfields)
        return self


class PageInfoFields(GraphQLField):
    has_next_page: PageInfoGraphQLField = PageInfoGraphQLField("hasNextPage")
    has_previous_page: PageInfoGraphQLField = PageInfoGraphQLField("hasPreviousPage")
    start_cursor: PageInfoGraphQLField = PageInfoGraphQLField("startCursor")
    end_cursor: PageInfoGraphQLField = PageInfoGraphQLField("endCursor")

    def fields(self, *subfields: PageInfoGraphQLField) -> "PageInfoFields":
        self._subfields.extend(subfields)
        return self


class ProductFields(GraphQLField):
    id: ProductGraphQLField = ProductGraphQLField("id")
    slug: ProductGraphQLField = ProductGraphQLField("slug")
    name: ProductGraphQLField = ProductGraphQLField("name")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    private_metafield: ProductGraphQLField = ProductGraphQLField("privateMetafield")

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    metafield: ProductGraphQLField = ProductGraphQLField("metafield")

    def fields(
        self, *subfields: Union[ProductGraphQLField, "MetadataItemFields"]
    ) -> "ProductFields":
        self._subfields.extend(subfields)
        return self


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


class ProductTranslatableContentFields(GraphQLField):
    id: ProductTranslatableContentGraphQLField = ProductTranslatableContentGraphQLField(
        "id"
    )
    product_id: ProductTranslatableContentGraphQLField = (
        ProductTranslatableContentGraphQLField("productId")
    )
    seo_title: ProductTranslatableContentGraphQLField = (
        ProductTranslatableContentGraphQLField("seoTitle")
    )
    seo_description: ProductTranslatableContentGraphQLField = (
        ProductTranslatableContentGraphQLField("seoDescription")
    )
    name: ProductTranslatableContentGraphQLField = (
        ProductTranslatableContentGraphQLField("name")
    )
    description: ProductTranslatableContentGraphQLField = (
        ProductTranslatableContentGraphQLField("description")
    )

    def fields(
        self, *subfields: ProductTranslatableContentGraphQLField
    ) -> "ProductTranslatableContentFields":
        self._subfields.extend(subfields)
        return self


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


class TranslatableItemConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "TranslatableItemEdgeFields":
        return TranslatableItemEdgeFields("edges")

    total_count: TranslatableItemConnectionGraphQLField = (
        TranslatableItemConnectionGraphQLField("totalCount")
    )

    def fields(
        self,
        *subfields: Union[
            TranslatableItemConnectionGraphQLField,
            "PageInfoFields",
            "TranslatableItemEdgeFields",
        ]
    ) -> "TranslatableItemConnectionFields":
        self._subfields.extend(subfields)
        return self


class TranslatableItemEdgeFields(GraphQLField):
    node: TranslatableItemUnion = TranslatableItemUnion("node")
    cursor: TranslatableItemEdgeGraphQLField = TranslatableItemEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self,
        *subfields: Union[TranslatableItemEdgeGraphQLField, "TranslatableItemUnion"]
    ) -> "TranslatableItemEdgeFields":
        self._subfields.extend(subfields)
        return self


class UpdateMetadataFields(GraphQLField):
    @classmethod
    def metadata_errors(cls) -> "MetadataErrorFields":
        return MetadataErrorFields("metadata_errors")

    @classmethod
    def errors(cls) -> "MetadataErrorFields":
        return MetadataErrorFields("errors")

    item: ObjectWithMetadataInterface = ObjectWithMetadataInterface("item")

    def fields(
        self,
        *subfields: Union[
            UpdateMetadataGraphQLField,
            "MetadataErrorFields",
            "ObjectWithMetadataInterface",
        ]
    ) -> "UpdateMetadataFields":
        self._subfields.extend(subfields)
        return self
