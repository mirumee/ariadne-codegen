from typing import Optional, Union

from . import (
    AdminGraphQLField,
    GuestGraphQLField,
    PersonGraphQLField,
    PostGraphQLField,
    UserGraphQLField,
)
from .base_operation import GraphQLField


class AdminFields(GraphQLField):
    id: AdminGraphQLField = AdminGraphQLField("id")
    name: AdminGraphQLField = AdminGraphQLField("name")
    email: AdminGraphQLField = AdminGraphQLField("email")
    privileges: AdminGraphQLField = AdminGraphQLField("privileges")
    created_at: AdminGraphQLField = AdminGraphQLField("createdAt")

    @classmethod
    def metafield(cls, *, key: Optional[str] = None) -> "AdminGraphQLField":
        return AdminGraphQLField("metafield", key=key)

    def fields(self, *subfields: AdminGraphQLField) -> "AdminFields":
        self._subfields.extend(subfields)
        return self


class GuestFields(GraphQLField):
    id: GuestGraphQLField = GuestGraphQLField("id")
    name: GuestGraphQLField = GuestGraphQLField("name")
    email: GuestGraphQLField = GuestGraphQLField("email")
    visit_count: GuestGraphQLField = GuestGraphQLField("visitCount")
    created_at: GuestGraphQLField = GuestGraphQLField("createdAt")

    @classmethod
    def metafield(cls, *, key: Optional[str] = None) -> "GuestGraphQLField":
        return GuestGraphQLField("metafield", key=key)

    def fields(self, *subfields: GuestGraphQLField) -> "GuestFields":
        self._subfields.extend(subfields)
        return self


class PersonInterface(GraphQLField):
    id: PersonGraphQLField = PersonGraphQLField("id")
    name: PersonGraphQLField = PersonGraphQLField("name")
    email: PersonGraphQLField = PersonGraphQLField("email")

    @classmethod
    def metafield(cls, *, key: Optional[str] = None) -> "PersonGraphQLField":
        return PersonGraphQLField("metafield", key=key)

    def fields(self, *subfields: PersonGraphQLField) -> "PersonInterface":
        self._subfields.extend(subfields)
        return self

    def on(self, type_name: str, *subfields: GraphQLField) -> "PersonInterface":
        self._inline_fragments[type_name] = subfields
        return self


class PostFields(GraphQLField):
    id: PostGraphQLField = PostGraphQLField("id")
    title: PostGraphQLField = PostGraphQLField("title")
    content: PostGraphQLField = PostGraphQLField("content")

    @classmethod
    def author(cls) -> "PersonInterface":
        return PersonInterface("author")

    published_at: PostGraphQLField = PostGraphQLField("publishedAt")

    def fields(
        self, *subfields: Union[PostGraphQLField, "PersonInterface"]
    ) -> "PostFields":
        self._subfields.extend(subfields)
        return self


class UserFields(GraphQLField):
    id: UserGraphQLField = UserGraphQLField("id")
    name: UserGraphQLField = UserGraphQLField("name")
    email: UserGraphQLField = UserGraphQLField("email")
    age: UserGraphQLField = UserGraphQLField("age")
    role: UserGraphQLField = UserGraphQLField("role")

    @classmethod
    def friends(cls) -> "UserFields":
        return UserFields("friends")

    created_at: UserGraphQLField = UserGraphQLField("createdAt")

    @classmethod
    def metafield(cls, *, key: Optional[str] = None) -> "UserGraphQLField":
        return UserGraphQLField("metafield", key=key)

    def fields(self, *subfields: Union[UserGraphQLField, "UserFields"]) -> "UserFields":
        self._subfields.extend(subfields)
        return self
