from typing import Any, Dict, Optional, Union

from .base_operation import GraphQLField
from .custom_typing_fields import (
    AdminGraphQLField,
    GuestGraphQLField,
    PersonInterfaceGraphQLField,
    PostGraphQLField,
    UserGraphQLField,
)


class AdminFields(GraphQLField):
    id: "AdminGraphQLField" = AdminGraphQLField("id")
    name: "AdminGraphQLField" = AdminGraphQLField("name")
    privileges: "AdminGraphQLField" = AdminGraphQLField("privileges")
    email: "AdminGraphQLField" = AdminGraphQLField("email")
    created_at: "AdminGraphQLField" = AdminGraphQLField("createdAt")

    @classmethod
    def metafield(cls, key: str) -> "AdminGraphQLField":
        arguments: Dict[str, Dict[str, Any]] = {
            "key": {"type": "String!", "value": key}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AdminGraphQLField("metafield", arguments=cleared_arguments)

    @classmethod
    def custom_field(cls, *, key: Optional[str] = None) -> "AdminGraphQLField":
        arguments: Dict[str, Dict[str, Any]] = {"key": {"type": "String", "value": key}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return AdminGraphQLField("custom_field", arguments=cleared_arguments)

    def fields(self, *subfields: AdminGraphQLField) -> "AdminFields":
        """Subfields should come from the AdminFields class"""
        self._subfields.extend(subfields)
        return self


class GuestFields(GraphQLField):
    id: "GuestGraphQLField" = GuestGraphQLField("id")
    name: "GuestGraphQLField" = GuestGraphQLField("name")
    visit_count: "GuestGraphQLField" = GuestGraphQLField("visitCount")
    email: "GuestGraphQLField" = GuestGraphQLField("email")
    created_at: "GuestGraphQLField" = GuestGraphQLField("createdAt")

    @classmethod
    def metafield(cls, key: str) -> "GuestGraphQLField":
        arguments: Dict[str, Dict[str, Any]] = {
            "key": {"type": "String!", "value": key}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GuestGraphQLField("metafield", arguments=cleared_arguments)

    def fields(self, *subfields: GuestGraphQLField) -> "GuestFields":
        """Subfields should come from the GuestFields class"""
        self._subfields.extend(subfields)
        return self


class PersonInterfaceInterface(GraphQLField):
    id: "PersonInterfaceGraphQLField" = PersonInterfaceGraphQLField("id")
    name: "PersonInterfaceGraphQLField" = PersonInterfaceGraphQLField("name")
    email: "PersonInterfaceGraphQLField" = PersonInterfaceGraphQLField("email")

    @classmethod
    def metafield(cls, key: str) -> "PersonInterfaceGraphQLField":
        arguments: Dict[str, Dict[str, Any]] = {
            "key": {"type": "String!", "value": key}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return PersonInterfaceGraphQLField("metafield", arguments=cleared_arguments)

    def fields(
        self, *subfields: PersonInterfaceGraphQLField
    ) -> "PersonInterfaceInterface":
        """Subfields should come from the PersonInterfaceInterface class"""
        self._subfields.extend(subfields)
        return self

    def on(
        self, type_name: str, *subfields: GraphQLField
    ) -> "PersonInterfaceInterface":
        self._inline_fragments[type_name] = subfields
        return self


class PostFields(GraphQLField):
    id: "PostGraphQLField" = PostGraphQLField("id")
    title: "PostGraphQLField" = PostGraphQLField("title")
    content: "PostGraphQLField" = PostGraphQLField("content")

    @classmethod
    def author(cls) -> "PersonInterfaceInterface":
        return PersonInterfaceInterface("author")

    published_at: "PostGraphQLField" = PostGraphQLField("publishedAt")

    def fields(
        self, *subfields: Union[PostGraphQLField, "PersonInterfaceInterface"]
    ) -> "PostFields":
        """Subfields should come from the PostFields class"""
        self._subfields.extend(subfields)
        return self


class UserFields(GraphQLField):
    id: "UserGraphQLField" = UserGraphQLField("id")
    name: "UserGraphQLField" = UserGraphQLField("name")
    age: "UserGraphQLField" = UserGraphQLField("age")
    email: "UserGraphQLField" = UserGraphQLField("email")
    role: "UserGraphQLField" = UserGraphQLField("role")
    created_at: "UserGraphQLField" = UserGraphQLField("createdAt")

    @classmethod
    def friends(cls) -> "UserFields":
        return UserFields("friends")

    @classmethod
    def metafield(cls, key: str) -> "UserGraphQLField":
        arguments: Dict[str, Dict[str, Any]] = {
            "key": {"type": "String!", "value": key}
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UserGraphQLField("metafield", arguments=cleared_arguments)

    def fields(self, *subfields: Union[UserGraphQLField, "UserFields"]) -> "UserFields":
        """Subfields should come from the UserFields class"""
        self._subfields.extend(subfields)
        return self
