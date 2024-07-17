from .base_operation import GraphQLField


class PersonInterfaceGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "PersonInterfaceGraphQLField":
        self._alias = alias
        return self


class UserGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "UserGraphQLField":
        self._alias = alias
        return self


class AdminGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "AdminGraphQLField":
        self._alias = alias
        return self


class GuestGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "GuestGraphQLField":
        self._alias = alias
        return self


class PostGraphQLField(GraphQLField):
    def alias(self, alias: str) -> "PostGraphQLField":
        self._alias = alias
        return self


class SearchResultUnion(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "SearchResultUnion":
        self._inline_fragments[type_name] = subfields
        return self

    def alias(self, alias: str) -> "SearchResultUnion":
        self._alias = alias
        return self
