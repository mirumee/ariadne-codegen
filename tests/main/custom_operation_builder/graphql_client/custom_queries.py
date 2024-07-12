from typing import Optional

from .custom_fields import PersonInterfaceInterface, PostFields, UserFields
from .custom_typing_fields import GraphQLField, SearchResultUnion


class Query:
    @classmethod
    def hello(cls) -> GraphQLField:
        arguments = {}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="hello", arguments=cleared_arguments)

    @classmethod
    def greeting(cls, *, name: Optional[str] = None) -> GraphQLField:
        arguments = {"name": {"type": "String", "value": name}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return GraphQLField(field_name="greeting", arguments=cleared_arguments)

    @classmethod
    def user(cls, user_id: str) -> UserFields:
        arguments = {"user_id": {"type": "ID!", "value": user_id}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UserFields(field_name="user", arguments=cleared_arguments)

    @classmethod
    def users(cls) -> UserFields:
        arguments = {}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UserFields(field_name="users", arguments=cleared_arguments)

    @classmethod
    def search(cls, text: str) -> SearchResultUnion:
        arguments = {"text": {"type": "String!", "value": text}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return SearchResultUnion(field_name="search", arguments=cleared_arguments)

    @classmethod
    def posts(cls) -> PostFields:
        arguments = {}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return PostFields(field_name="posts", arguments=cleared_arguments)

    @classmethod
    def person(cls, person_id: str) -> PersonInterfaceInterface:
        arguments = {"person_id": {"type": "ID!", "value": person_id}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return PersonInterfaceInterface(
            field_name="person", arguments=cleared_arguments
        )

    @classmethod
    def people(cls) -> PersonInterfaceInterface:
        arguments = {}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return PersonInterfaceInterface(
            field_name="people", arguments=cleared_arguments
        )
