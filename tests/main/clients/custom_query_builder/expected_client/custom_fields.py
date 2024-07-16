from typing import Any, Dict, Optional, Union

from .base_operation import GraphQLField
from .custom_typing_fields import (
    AppGraphQLField,
    CollectionTranslatableContentGraphQLField,
    MetadataErrorGraphQLField,
    MetadataItemGraphQLField,
    ObjectWithMetadataGraphQLField,
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


class AppFields(GraphQLField):
    id: "AppGraphQLField" = AppGraphQLField("id")

    def fields(self, *subfields: AppGraphQLField) -> "AppFields":
        """Subfields should come from the AppFields class"""
        self._subfields.extend(subfields)
        return self


class CollectionTranslatableContentFields(GraphQLField):
    id: "CollectionTranslatableContentGraphQLField" = (
        CollectionTranslatableContentGraphQLField("id")
    )
    collection_id: "CollectionTranslatableContentGraphQLField" = (
        CollectionTranslatableContentGraphQLField("collectionId")
    )
    seo_title: "CollectionTranslatableContentGraphQLField" = (
        CollectionTranslatableContentGraphQLField("seoTitle")
    )
    seo_description: "CollectionTranslatableContentGraphQLField" = (
        CollectionTranslatableContentGraphQLField("seoDescription")
    )
    name: "CollectionTranslatableContentGraphQLField" = (
        CollectionTranslatableContentGraphQLField("name")
    )
    description: "CollectionTranslatableContentGraphQLField" = (
        CollectionTranslatableContentGraphQLField("description")
    )

    def fields(
        self, *subfields: CollectionTranslatableContentGraphQLField
    ) -> "CollectionTranslatableContentFields":
        """Subfields should come from the CollectionTranslatableContentFields class"""
        self._subfields.extend(subfields)
        return self


class MetadataErrorFields(GraphQLField):
    field: "MetadataErrorGraphQLField" = MetadataErrorGraphQLField("field")
    message: "MetadataErrorGraphQLField" = MetadataErrorGraphQLField("message")
    code: "MetadataErrorGraphQLField" = MetadataErrorGraphQLField("code")

    def fields(self, *subfields: MetadataErrorGraphQLField) -> "MetadataErrorFields":
        """Subfields should come from the MetadataErrorFields class"""
        self._subfields.extend(subfields)
        return self


class MetadataItemFields(GraphQLField):
    key: "MetadataItemGraphQLField" = MetadataItemGraphQLField("key")
    value: "MetadataItemGraphQLField" = MetadataItemGraphQLField("value")

    def fields(self, *subfields: MetadataItemGraphQLField) -> "MetadataItemFields":
        """Subfields should come from the MetadataItemFields class"""
        self._subfields.extend(subfields)
        return self


class ObjectWithMetadataInterface(GraphQLField):
    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    @classmethod
    def private_metafield(cls, key: str) -> "ObjectWithMetadataGraphQLField":
        arguments: Dict[str, Dict[str, Any]] = {
            "key": {"type": "String!", "value": key}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ObjectWithMetadataGraphQLField(
            "private_metafield", arguments=cleared_arguments
        )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    @classmethod
    def metafield(cls, key: str) -> "ObjectWithMetadataGraphQLField":
        arguments: Dict[str, Dict[str, Any]] = {
            "key": {"type": "String!", "value": key}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ObjectWithMetadataGraphQLField("metafield", arguments=cleared_arguments)

    def fields(
        self, *subfields: Union[ObjectWithMetadataGraphQLField, "MetadataItemFields"]
    ) -> "ObjectWithMetadataInterface":
        """Subfields should come from the ObjectWithMetadataInterface class"""
        self._subfields.extend(subfields)
        return self

    def on(
        self, type_name: str, *subfields: GraphQLField
    ) -> "ObjectWithMetadataInterface":
        self._inline_fragments[type_name] = subfields
        return self


class PageInfoFields(GraphQLField):
    has_next_page: "PageInfoGraphQLField" = PageInfoGraphQLField("hasNextPage")
    has_previous_page: "PageInfoGraphQLField" = PageInfoGraphQLField("hasPreviousPage")
    start_cursor: "PageInfoGraphQLField" = PageInfoGraphQLField("startCursor")
    end_cursor: "PageInfoGraphQLField" = PageInfoGraphQLField("endCursor")

    def fields(self, *subfields: PageInfoGraphQLField) -> "PageInfoFields":
        """Subfields should come from the PageInfoFields class"""
        self._subfields.extend(subfields)
        return self


class ProductFields(GraphQLField):
    id: "ProductGraphQLField" = ProductGraphQLField("id")
    slug: "ProductGraphQLField" = ProductGraphQLField("slug")
    name: "ProductGraphQLField" = ProductGraphQLField("name")

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("private_metadata")

    @classmethod
    def private_metafield(cls, key: str) -> "ProductGraphQLField":
        arguments: Dict[str, Dict[str, Any]] = {
            "key": {"type": "String!", "value": key}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ProductGraphQLField("private_metafield", arguments=cleared_arguments)

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        return MetadataItemFields("metadata")

    @classmethod
    def metafield(cls, key: str) -> "ProductGraphQLField":
        arguments: Dict[str, Dict[str, Any]] = {
            "key": {"type": "String!", "value": key}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ProductGraphQLField("metafield", arguments=cleared_arguments)

    def fields(
        self, *subfields: Union[ProductGraphQLField, "MetadataItemFields"]
    ) -> "ProductFields":
        """Subfields should come from the ProductFields class"""
        self._subfields.extend(subfields)
        return self


class ProductCountableConnectionFields(GraphQLField):
    @classmethod
    def edges(cls) -> "ProductCountableEdgeFields":
        return ProductCountableEdgeFields("edges")

    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    total_count: "ProductCountableConnectionGraphQLField" = (
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
        """Subfields should come from the ProductCountableConnectionFields class"""
        self._subfields.extend(subfields)
        return self


class ProductCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "ProductFields":
        return ProductFields("node")

    cursor: "ProductCountableEdgeGraphQLField" = ProductCountableEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self, *subfields: Union[ProductCountableEdgeGraphQLField, "ProductFields"]
    ) -> "ProductCountableEdgeFields":
        """Subfields should come from the ProductCountableEdgeFields class"""
        self._subfields.extend(subfields)
        return self


class ProductTranslatableContentFields(GraphQLField):
    id: "ProductTranslatableContentGraphQLField" = (
        ProductTranslatableContentGraphQLField("id")
    )
    product_id: "ProductTranslatableContentGraphQLField" = (
        ProductTranslatableContentGraphQLField("productId")
    )
    seo_title: "ProductTranslatableContentGraphQLField" = (
        ProductTranslatableContentGraphQLField("seoTitle")
    )
    seo_description: "ProductTranslatableContentGraphQLField" = (
        ProductTranslatableContentGraphQLField("seoDescription")
    )
    name: "ProductTranslatableContentGraphQLField" = (
        ProductTranslatableContentGraphQLField("name")
    )
    description: "ProductTranslatableContentGraphQLField" = (
        ProductTranslatableContentGraphQLField("description")
    )

    def fields(
        self, *subfields: ProductTranslatableContentGraphQLField
    ) -> "ProductTranslatableContentFields":
        """Subfields should come from the ProductTranslatableContentFields class"""
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
        """Subfields should come from the ProductTypeCountableConnectionFields class"""
        self._subfields.extend(subfields)
        return self


class TranslatableItemConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("page_info")

    @classmethod
    def edges(cls) -> "TranslatableItemEdgeFields":
        return TranslatableItemEdgeFields("edges")

    total_count: "TranslatableItemConnectionGraphQLField" = (
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
        """Subfields should come from the TranslatableItemConnectionFields class"""
        self._subfields.extend(subfields)
        return self


class TranslatableItemEdgeFields(GraphQLField):
    node: "TranslatableItemUnion" = TranslatableItemUnion("node")
    cursor: "TranslatableItemEdgeGraphQLField" = TranslatableItemEdgeGraphQLField(
        "cursor"
    )

    def fields(
        self,
        *subfields: Union[TranslatableItemEdgeGraphQLField, "TranslatableItemUnion"]
    ) -> "TranslatableItemEdgeFields":
        """Subfields should come from the TranslatableItemEdgeFields class"""
        self._subfields.extend(subfields)
        return self


class UpdateMetadataFields(GraphQLField):
    @classmethod
    def metadata_errors(cls) -> "MetadataErrorFields":
        return MetadataErrorFields("metadata_errors")

    @classmethod
    def errors(cls) -> "MetadataErrorFields":
        return MetadataErrorFields("errors")

    @classmethod
    def item(cls) -> "ObjectWithMetadataInterface":
        return ObjectWithMetadataInterface("item")

    def fields(
        self,
        *subfields: Union[
            UpdateMetadataGraphQLField,
            "MetadataErrorFields",
            "ObjectWithMetadataInterface",
        ]
    ) -> "UpdateMetadataFields":
        """Subfields should come from the UpdateMetadataFields class"""
        self._subfields.extend(subfields)
        return self
