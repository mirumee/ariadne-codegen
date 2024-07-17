from .base_operation import GraphQLField


class ProductGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "ProductGraphQLField":
        self._alias = alias
        return self


class ProductCountableEdgeGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "ProductCountableEdgeGraphQLField":
        self._alias = alias
        return self


class ProductCountableConnectionGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "ProductCountableConnectionGraphQLField":
        self._alias = alias
        return self


class AppGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "AppGraphQLField":
        self._alias = alias
        return self


class ProductTypeCountableConnectionGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "ProductTypeCountableConnectionGraphQLField":
        self._alias = alias
        return self


class PageInfoGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "PageInfoGraphQLField":
        self._alias = alias
        return self


class ObjectWithMetadataGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "ObjectWithMetadataGraphQLField":
        self._alias = alias
        return self


class MetadataItemGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "MetadataItemGraphQLField":
        self._alias = alias
        return self


class UpdateMetadataGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "UpdateMetadataGraphQLField":
        self._alias = alias
        return self


class MetadataErrorGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "MetadataErrorGraphQLField":
        self._alias = alias
        return self


class TranslatableItemConnectionGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "TranslatableItemConnectionGraphQLField":
        self._alias = alias
        return self


class TranslatableItemEdgeGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "TranslatableItemEdgeGraphQLField":
        self._alias = alias
        return self


class TranslatableItemUnion(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "TranslatableItemUnion":
        self._inline_fragments[type_name] = subfields
        return self

    def alias(self, alias: str) -> "TranslatableItemUnion":
        self._alias = alias
        return self


class ProductTranslatableContentGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "ProductTranslatableContentGraphQLField":
        self._alias = alias
        return self


class CollectionTranslatableContentGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "CollectionTranslatableContentGraphQLField":
        self._alias = alias
        return self
