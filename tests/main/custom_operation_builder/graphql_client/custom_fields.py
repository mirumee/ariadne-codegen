from typing import Any, Optional, Union

from . import (
    AdminGraphQLField,
    GuestGraphQLField,
    PersonInterfaceGraphQLField,
    PostGraphQLField,
    UserGraphQLField,
)
from .base_operation import GraphQLField


class AdminFields(GraphQLField):
    id: AdminGraphQLField = AdminGraphQLField("id")
    name: AdminGraphQLField = AdminGraphQLField("name")
    privileges: AdminGraphQLField = AdminGraphQLField("privileges")
    email: AdminGraphQLField = AdminGraphQLField("email")
    created_at: AdminGraphQLField = AdminGraphQLField("createdAt")

    @classmethod
    def metafield(cls, key: str) -> "AdminGraphQLField":
        return AdminGraphQLField(
            "metafield", arguments={"key": {"type": "String!", "value": key}}
        )

    def fields(self, *subfields: AdminGraphQLField) -> "AdminFields":
        self._subfields.extend(subfields)
        return self


class GuestFields(GraphQLField):
    id: GuestGraphQLField = GuestGraphQLField("id")
    name: GuestGraphQLField = GuestGraphQLField("name")
    visit_count: GuestGraphQLField = GuestGraphQLField("visitCount")
    email: GuestGraphQLField = GuestGraphQLField("email")
    created_at: GuestGraphQLField = GuestGraphQLField("createdAt")

    @classmethod
    def metafield(cls, key: str) -> "GuestGraphQLField":
        return GuestGraphQLField(
            "metafield", arguments={"key": {"type": "String!", "value": key}}
        )

    def fields(self, *subfields: GuestGraphQLField) -> "GuestFields":
        self._subfields.extend(subfields)
        return self


class PersonInterfaceInterface(GraphQLField):
    id: PersonInterfaceGraphQLField = PersonInterfaceGraphQLField("id")
    name: PersonInterfaceGraphQLField = PersonInterfaceGraphQLField("name")
    email: PersonInterfaceGraphQLField = PersonInterfaceGraphQLField("email")

    @classmethod
    def metafield(cls, key: str) -> "PersonInterfaceGraphQLField":
        return PersonInterfaceGraphQLField(
            "metafield", arguments={"key": {"type": "String!", "value": key}}
        )

    def fields(
        self, *subfields: PersonInterfaceGraphQLField
    ) -> "PersonInterfaceInterface":
        self._subfields.extend(subfields)
        return self

    def on(
        self, type_name: str, *subfields: GraphQLField
    ) -> "PersonInterfaceInterface":
        self._inline_fragments[type_name] = subfields
        return self


class PostFields(GraphQLField):
    id: PostGraphQLField = PostGraphQLField("id")
    title: PostGraphQLField = PostGraphQLField("title")
    content: PostGraphQLField = PostGraphQLField("content")

    @classmethod
    def author(cls) -> "PersonInterfaceInterface":
        return PersonInterfaceInterface("author", arguments={})

    published_at: PostGraphQLField = PostGraphQLField("publishedAt")

    def fields(
        self, *subfields: Union[PostGraphQLField, "PersonInterfaceInterface"]
    ) -> "PostFields":
        self._subfields.extend(subfields)
        return self


class UserFields(GraphQLField):
    id: UserGraphQLField = UserGraphQLField("id")
    name: UserGraphQLField = UserGraphQLField("name")
    age: UserGraphQLField = UserGraphQLField("age")
    email: UserGraphQLField = UserGraphQLField("email")
    role: UserGraphQLField = UserGraphQLField("role")
    created_at: UserGraphQLField = UserGraphQLField("createdAt")

    @classmethod
    def friends(cls) -> "UserFields":
        return UserFields("friends", arguments={})

    @classmethod
    def metafield(cls, key: str) -> "UserGraphQLField":
        return UserGraphQLField(
            "metafield", arguments={"key": {"type": "String!", "value": key}}
        )

    def fields(self, *subfields: Union[UserGraphQLField, "UserFields"]) -> "UserFields":
        self._subfields.extend(subfields)
        return self
