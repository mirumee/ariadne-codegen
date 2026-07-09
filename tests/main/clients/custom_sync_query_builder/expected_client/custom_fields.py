from typing import Any, Union

from .base_operation import GraphQLField, GraphQLLeafField
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
    id = GraphQLLeafField("id", AppGraphQLField)

    def fields(self, *subfields: AppGraphQLField) -> "AppFields":
        """Subfields should come from the AppFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "AppFields":
        self._alias = alias
        return self


class CollectionTranslatableContentFields(GraphQLField):
    id = GraphQLLeafField("id", CollectionTranslatableContentGraphQLField)
    "The ID of the collection translatable content."
    collection_id = GraphQLLeafField(
        "collectionId", CollectionTranslatableContentGraphQLField
    )
    "The ID of the collection to translate.\n\nAdded in Saleor 3.14."
    seo_title = GraphQLLeafField("seoTitle", CollectionTranslatableContentGraphQLField)
    "SEO title to translate."
    seo_description = GraphQLLeafField(
        "seoDescription", CollectionTranslatableContentGraphQLField
    )
    "SEO description to translate."
    name = GraphQLLeafField("name", CollectionTranslatableContentGraphQLField)
    "Collection's name to translate."
    description = GraphQLLeafField(
        "description", CollectionTranslatableContentGraphQLField
    )
    "Collection's description to translate.\n\nRich text format. For reference see https://editorjs.io/"

    def fields(
        self, *subfields: CollectionTranslatableContentGraphQLField
    ) -> "CollectionTranslatableContentFields":
        """Subfields should come from the CollectionTranslatableContentFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "CollectionTranslatableContentFields":
        self._alias = alias
        return self


class MetadataErrorFields(GraphQLField):
    field = GraphQLLeafField("field", MetadataErrorGraphQLField)
    "Name of a field that caused the error. A value of `null` indicates that the error isn't associated with a particular field."
    message = GraphQLLeafField("message", MetadataErrorGraphQLField)
    "The error message."
    code = GraphQLLeafField("code", MetadataErrorGraphQLField)
    "The error code."

    def fields(self, *subfields: MetadataErrorGraphQLField) -> "MetadataErrorFields":
        """Subfields should come from the MetadataErrorFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "MetadataErrorFields":
        self._alias = alias
        return self


class MetadataItemFields(GraphQLField):
    key = GraphQLLeafField("key", MetadataItemGraphQLField)
    "Key of a metadata item."
    value = GraphQLLeafField("value", MetadataItemGraphQLField)
    "Value of a metadata item."

    def fields(self, *subfields: MetadataItemGraphQLField) -> "MetadataItemFields":
        """Subfields should come from the MetadataItemFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "MetadataItemFields":
        self._alias = alias
        return self


class ObjectWithMetadataInterface(GraphQLField):
    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        """list of private metadata items. Requires staff permissions to access."""
        return MetadataItemFields("privateMetadata")

    @classmethod
    def private_metafield(cls, key: str) -> "ObjectWithMetadataGraphQLField":
        """A single key from private metadata. Requires staff permissions to access.

        Tip: Use GraphQL aliases to fetch multiple keys."""
        arguments: dict[str, dict[str, Any]] = {
            "key": {"type": "String!", "value": key}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ObjectWithMetadataGraphQLField(
            "privateMetafield", arguments=cleared_arguments
        )

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        """list of public metadata items. Can be accessed without permissions."""
        return MetadataItemFields("metadata")

    @classmethod
    def metafield(cls, key: str) -> "ObjectWithMetadataGraphQLField":
        """A single key from public metadata.

        Tip: Use GraphQL aliases to fetch multiple keys."""
        arguments: dict[str, dict[str, Any]] = {
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

    def alias(self, alias: str) -> "ObjectWithMetadataInterface":
        self._alias = alias
        return self

    def on(
        self, type_name: str, *subfields: GraphQLField
    ) -> "ObjectWithMetadataInterface":
        self._inline_fragments[type_name] = subfields
        return self


class PageInfoFields(GraphQLField):
    has_next_page = GraphQLLeafField("hasNextPage", PageInfoGraphQLField)
    has_previous_page = GraphQLLeafField("hasPreviousPage", PageInfoGraphQLField)
    start_cursor = GraphQLLeafField("startCursor", PageInfoGraphQLField)
    end_cursor = GraphQLLeafField("endCursor", PageInfoGraphQLField)

    def fields(self, *subfields: PageInfoGraphQLField) -> "PageInfoFields":
        """Subfields should come from the PageInfoFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "PageInfoFields":
        self._alias = alias
        return self


class ProductFields(GraphQLField):
    id = GraphQLLeafField("id", ProductGraphQLField)
    slug = GraphQLLeafField("slug", ProductGraphQLField)
    name = GraphQLLeafField("name", ProductGraphQLField)

    @classmethod
    def private_metadata(cls) -> "MetadataItemFields":
        """list of private metadata items. Requires staff permissions to access."""
        return MetadataItemFields("privateMetadata")

    @classmethod
    def private_metafield(cls, key: str) -> "ProductGraphQLField":
        """A single key from private metadata. Requires staff permissions to access.

        Tip: Use GraphQL aliases to fetch multiple keys."""
        arguments: dict[str, dict[str, Any]] = {
            "key": {"type": "String!", "value": key}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return ProductGraphQLField("privateMetafield", arguments=cleared_arguments)

    @classmethod
    def metadata(cls) -> "MetadataItemFields":
        """list of public metadata items. Can be accessed without permissions."""
        return MetadataItemFields("metadata")

    @classmethod
    def metafield(cls, key: str) -> "ProductGraphQLField":
        """A single key from public metadata.

        Tip: Use GraphQL aliases to fetch multiple keys."""
        arguments: dict[str, dict[str, Any]] = {
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

    def alias(self, alias: str) -> "ProductFields":
        self._alias = alias
        return self


class ProductCountableConnectionFields(GraphQLField):
    @classmethod
    def edges(cls) -> "ProductCountableEdgeFields":
        return ProductCountableEdgeFields("edges")

    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("pageInfo")

    total_count = GraphQLLeafField("totalCount", ProductCountableConnectionGraphQLField)

    def fields(
        self,
        *subfields: Union[
            ProductCountableConnectionGraphQLField,
            "PageInfoFields",
            "ProductCountableEdgeFields",
        ],
    ) -> "ProductCountableConnectionFields":
        """Subfields should come from the ProductCountableConnectionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProductCountableConnectionFields":
        self._alias = alias
        return self


class ProductCountableEdgeFields(GraphQLField):
    @classmethod
    def node(cls) -> "ProductFields":
        return ProductFields("node")

    cursor = GraphQLLeafField("cursor", ProductCountableEdgeGraphQLField)

    def fields(
        self, *subfields: Union[ProductCountableEdgeGraphQLField, "ProductFields"]
    ) -> "ProductCountableEdgeFields":
        """Subfields should come from the ProductCountableEdgeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProductCountableEdgeFields":
        self._alias = alias
        return self


class ProductTranslatableContentFields(GraphQLField):
    id = GraphQLLeafField("id", ProductTranslatableContentGraphQLField)
    "The ID of the product translatable content."
    product_id = GraphQLLeafField("productId", ProductTranslatableContentGraphQLField)
    "The ID of the product to translate.\n\nAdded in Saleor 3.14."
    seo_title = GraphQLLeafField("seoTitle", ProductTranslatableContentGraphQLField)
    "SEO title to translate."
    seo_description = GraphQLLeafField(
        "seoDescription", ProductTranslatableContentGraphQLField
    )
    "SEO description to translate."
    name = GraphQLLeafField("name", ProductTranslatableContentGraphQLField)
    "Product's name to translate."
    description = GraphQLLeafField(
        "description", ProductTranslatableContentGraphQLField
    )
    "Product's description to translate.\n\nRich text format. For reference see https://editorjs.io/"

    def fields(
        self, *subfields: ProductTranslatableContentGraphQLField
    ) -> "ProductTranslatableContentFields":
        """Subfields should come from the ProductTranslatableContentFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProductTranslatableContentFields":
        self._alias = alias
        return self


class ProductTypeCountableConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        return PageInfoFields("pageInfo")

    def fields(
        self,
        *subfields: Union[ProductTypeCountableConnectionGraphQLField, "PageInfoFields"],
    ) -> "ProductTypeCountableConnectionFields":
        """Subfields should come from the ProductTypeCountableConnectionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "ProductTypeCountableConnectionFields":
        self._alias = alias
        return self


class TranslatableItemConnectionFields(GraphQLField):
    @classmethod
    def page_info(cls) -> "PageInfoFields":
        """Pagination data for this connection."""
        return PageInfoFields("pageInfo")

    @classmethod
    def edges(cls) -> "TranslatableItemEdgeFields":
        return TranslatableItemEdgeFields("edges")

    total_count = GraphQLLeafField("totalCount", TranslatableItemConnectionGraphQLField)
    "A total count of items in the collection."

    def fields(
        self,
        *subfields: Union[
            TranslatableItemConnectionGraphQLField,
            "PageInfoFields",
            "TranslatableItemEdgeFields",
        ],
    ) -> "TranslatableItemConnectionFields":
        """Subfields should come from the TranslatableItemConnectionFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TranslatableItemConnectionFields":
        self._alias = alias
        return self


class TranslatableItemEdgeFields(GraphQLField):
    node = GraphQLLeafField("node", TranslatableItemUnion)
    "The item at the end of the edge."
    cursor = GraphQLLeafField("cursor", TranslatableItemEdgeGraphQLField)
    "A cursor for use in pagination."

    def fields(
        self,
        *subfields: Union[TranslatableItemEdgeGraphQLField, "TranslatableItemUnion"],
    ) -> "TranslatableItemEdgeFields":
        """Subfields should come from the TranslatableItemEdgeFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "TranslatableItemEdgeFields":
        self._alias = alias
        return self


class UpdateMetadataFields(GraphQLField):
    @classmethod
    def metadata_errors(cls) -> "MetadataErrorFields":
        return MetadataErrorFields("metadataErrors")

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
        ],
    ) -> "UpdateMetadataFields":
        """Subfields should come from the UpdateMetadataFields class"""
        self._subfields.extend(subfields)
        return self

    def alias(self, alias: str) -> "UpdateMetadataFields":
        self._alias = alias
        return self
