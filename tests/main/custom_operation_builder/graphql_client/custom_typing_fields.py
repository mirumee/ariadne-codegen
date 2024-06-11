from .base_operation import GraphQLField


class PersonGraphQLField(GraphQLField):
    pass


class SearchResultUnion(GraphQLField):
    def on(self, type_name: str, *subfields: GraphQLField) -> "SearchResultUnion":
        self._inline_fragments[type_name] = subfields
        return self


class UserGraphQLField(GraphQLField):
    pass


class AdminGraphQLField(GraphQLField):
    pass


class GuestGraphQLField(GraphQLField):
    pass


class PostGraphQLField(GraphQLField):
    pass
