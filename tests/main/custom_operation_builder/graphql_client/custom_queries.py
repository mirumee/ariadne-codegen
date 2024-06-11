from typing import Optional

from .custom_fields import (
    AdminFields,
    GuestFields,
    PersonInterface,
    PostFields,
    UserFields,
)
from .custom_typing_fields import GraphQLField, SearchResultUnion


class Query:
    @classmethod
    def hello(cls) -> GraphQLField:
        return GraphQLField(field_name="hello")

    @classmethod
    def greeting(cls, *, name: Optional[str] = None) -> GraphQLField:
        return GraphQLField(field_name="greeting", name=name)

    @classmethod
    def user(cls, *, user_id: Optional[str] = None) -> UserFields:
        return UserFields(field_name="user", user_id=user_id)

    @classmethod
    def users(cls) -> UserFields:
        return UserFields(field_name="users")

    @classmethod
    def admin(cls, *, admin_id: Optional[str] = None) -> AdminFields:
        return AdminFields(field_name="admin", admin_id=admin_id)

    @classmethod
    def admins(cls) -> AdminFields:
        return AdminFields(field_name="admins")

    @classmethod
    def guest(cls, *, guest_id: Optional[str] = None) -> GuestFields:
        return GuestFields(field_name="guest", guest_id=guest_id)

    @classmethod
    def guests(cls) -> GuestFields:
        return GuestFields(field_name="guests")

    @classmethod
    def search(cls, *, text: Optional[str] = None) -> SearchResultUnion:
        return SearchResultUnion(field_name="search", text=text)

    @classmethod
    def posts(cls) -> PostFields:
        return PostFields(field_name="posts")

    @classmethod
    def post(cls, *, post_id: Optional[str] = None) -> PostFields:
        return PostFields(field_name="post", post_id=post_id)

    @classmethod
    def person(cls, *, person_id: Optional[str] = None) -> PersonInterface:
        return PersonInterface(field_name="person", person_id=person_id)

    @classmethod
    def people(cls) -> PersonInterface:
        return PersonInterface(field_name="people")
