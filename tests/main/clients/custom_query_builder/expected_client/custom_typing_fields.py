from .base_operation import GraphQLField


class ProductGraphQLField(GraphQLField):
    pass


class ProductCountableEdgeGraphQLField(GraphQLField):
    pass


class ProductCountableConnectionGraphQLField(GraphQLField):
    pass


class AppGraphQLField(GraphQLField):
    pass


class ProductTypeCountableConnectionGraphQLField(GraphQLField):
    pass


class PageInfoGraphQLField(GraphQLField):
    pass


class ObjectWithMetadataInterface(GraphQLField):
    def on(
        self, type_name: str, *subfields: GraphQLField
    ) -> "ObjectWithMetadataInterface":
        self._inline_fragments[type_name] = subfields
        return self


class MetadataItemGraphQLField(GraphQLField):
    pass


class UpdateMetadataGraphQLField(GraphQLField):
    pass


class MetadataErrorGraphQLField(GraphQLField):
    pass


class TranslatableItemConnectionGraphQLField(GraphQLField):
    pass


class TranslatableItemEdgeGraphQLField(GraphQLField):
    pass


class TranslatableItemUnion(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "TranslatableItemUnion":
        self._inline_fragments[type_name] = subfields
        return self


class ProductTranslatableContentGraphQLField(GraphQLField):
    pass


class CollectionTranslatableContentGraphQLField(GraphQLField):
    pass
