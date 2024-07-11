from typing import Optional

from .custom_fields import PersonInterface, PostFields, UserFields
from .custom_typing_fields import GraphQLField, SearchResultUnion


class Query:
    @classmethod
    def hello(cls) -> GraphQLField:
        return GraphQLField(field_name="hello", arguments={})

    @classmethod
    def greeting(cls, *, name: Optional[str] = None) -> GraphQLField:
        return GraphQLField(
            field_name="greeting", arguments={"name": {"type": "String", "value": name}}
        )

    @classmethod
    def user(cls, user_id: str) -> UserFields:
        return UserFields(
            field_name="user", arguments={"user_id": {"type": "ID!", "value": user_id}}
        )

    @classmethod
    def users(cls) -> UserFields:
        return UserFields(field_name="users", arguments={})

    @classmethod
    def search(cls, text: str) -> SearchResultUnion:
        return SearchResultUnion(
            field_name="search", arguments={"text": {"type": "String!", "value": text}}
        )

    @classmethod
    def posts(cls) -> PostFields:
        return PostFields(field_name="posts", arguments={})

    @classmethod
    def person(cls, person_id: str) -> PersonInterface:
        return PersonInterface(
            field_name="person",
            arguments={"person_id": {"type": "ID!", "value": person_id}},
        )

    @classmethod
    def people(cls) -> PersonInterface:
        return PersonInterface(field_name="people", arguments={})
